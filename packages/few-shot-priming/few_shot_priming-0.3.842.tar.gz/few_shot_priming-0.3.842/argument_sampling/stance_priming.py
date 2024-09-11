import pandas as pd
import json
from collections import defaultdict
from tqdm import tqdm
from few_shot_priming.experiments import load_splits
from sentence_transformers import SentenceTransformer, losses, SentencesDataset, datasets, util
from sentence_transformers.evaluation import BinaryClassificationEvaluator
from sentence_transformers.readers import InputExample
from scipy.spatial.distance import cosine

def preprocess_dataset(dataset):
    for split in dataset:
        dataset[split]["topic-text"] = dataset[split].apply(lambda record: record["topic"] + "[SEP]" + record["text"], axis=1)

def generate_test_dataset(df, three_classes=False):
    list1 = []
    list2 = []
    labels = []
    for topic, df_topic in df.groupby("topic"):
        df_stances = list(df_topic.groupby("stance"))
        if len(df_stances)<2 or (three_classes and len(df_stances)<3)   :
            continue
        df_stance_1 = df_stances[0][1]
        df_stance_2 = df_stances[1][1]
        if not len(df_stance_1) or not len(df_stance_2):
            continue

        if three_classes:
            df_stance_3 = df_stances[2][1]
            if not len(df_stance_3) and not len(df_stance_2):
                continue

        for i, argument in df_topic.iterrows():
            for j, argument_2 in df_topic.iterrows():
                if j>i:
                    list1.append(argument["topic-text"])
                    list2.append(argument_2["topic-text"])
                    if argument["stance"] == argument_2["stance"]:
                        label = 1
                    else:
                        label = 0
                    labels.append(label)

    return list1, list2, labels

def train(model, params, train_dataloader, evaluator=None, output_model_path=None):


    learning_rate = params["lr"]
    epochs = params["epochs"]
    train_loss = losses.ContrastiveLoss(model=model)
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        optimizer_params = {'lr' : learning_rate},
        output_path=output_model_path,
        epochs=epochs,
        evaluator=evaluator,
        save_best_model=True,
        evaluation_steps=1000
    )
    return model

def create_evaluator(df_test, three_examples=False):
    list1, list2, labels = generate_test_dataset(df_test, three_examples)
    evaluator = BinaryClassificationEvaluator(list1, list2, labels,show_progress_bar=True)
    return evaluator


def generate_training_examples(df_training, three_classes=False):
    contrastive_examples = []
    guid = 0
    for topic, df_topic in df_training.groupby("topic"):
        df_stances = list(df_topic.groupby("stance"))
        if len(df_stances)<2 or (three_classes and len(df_stances)<3):
            continue
        df_stance_1 = df_stances[0][1]
        df_stance_2 = df_stances[1][1]

        if not len(df_stance_1) or not len(df_stance_2):
            continue
        if three_classes:
            df_stance_3 = df_stances[2][1]
            if not len(df_stance_3) or not len(df_stance_2):
                continue
        for i, argument in df_topic.iterrows():
            for j, argument_2 in df_topic.iterrows():
                if j>i:
                    pair = [argument["topic-text"], argument_2["topic-text"]]
                    if argument["stance"] == argument_2["stance"]:
                        label = 1
                    else:
                        label = 0
                    guid = guid + 1
            contrastive_examples.append(InputExample(texts=pair, label=label, guid=guid))

    return contrastive_examples

def load_similarities(path_similarities):

    with open(path_similarities, "r") as file:
        similarities= json.load(file)
    similarities_with_int_idices = {}
    for key in similarities:
        similarities_with_int_idices[int(key)]= {}
    for key in similarities:
        for train_key in similarities[key]:
            similarities_with_int_idices[int(key)][int(train_key)] = similarities[key][train_key]
    return similarities_with_int_idices

def generate_similarity_matrix(experiment, debug=False):
    path_model = f"/bigwork/nhwpajjy/contrastive_learning/models/{experiment}-all-new"
    path_similarities = f"/bigwork/nhwpajjy/contrastive_learning/models/{experiment}-similarties.json"
    model = SentenceTransformer(path_model)
    dataset =  load_splits(experiment, oversample=False, validate=False )
    preprocess_dataset(dataset)
    test_text = dataset["test"]["topic-text"]
    training_text = dataset["training"]["topic-text"]
    test_embeddings = model.encode(test_text.values.tolist())
    training_embeddings = model.encode(training_text.values.tolist())
    cosine_scores = util.cos_sim(test_embeddings, training_embeddings)
    similarities = defaultdict(dict)
    i,j = 0, 0
    for _,test_record in tqdm(dataset["test"].iterrows()):
        for _,train_record in dataset["training"].iterrows():
            similarities[test_record["id"]][train_record["id"]] = float(cosine_scores[i,j])
            j = j + 1
        i = i + 1
        j = 0
    with open(path_similarities, "w") as file:
        json.dump(similarities, file )


def generate_most_similar_stance_arguments(experiment, different_topics, debug):
    path_similarities = f"/bigwork/nhwpajjy/contrastive_learning/models/{experiment}-similarties.json"
    similarities = load_similarities(path_similarities)
    dataset =  load_splits(experiment, oversample=False, validate=False, debug=debug)
    df_training = dataset["training"]
    all_samples = []
    if experiment == "vast":
        ks = [3, 6, 12, 24, 48, 96]
    else:
        ks = [2, 4, 8, 16, 32, 64]

    if different_topics:
        for _, test_record in dataset["test"].iterrows():
            instances_scores_map = similarities[test_record["id"]]
            df_training["score"] = df_training["id"].apply(lambda id: instances_scores_map[id])
            df_training.sort_values("score", ascending=False, inplace=True)
            for k in ks:
                topic_set = set()
                id_set = set()
                samples= []
                exists_enough_topics = True
                while len(samples) < k:
                    for _, training_record in df_training.iterrows():
                        if exists_enough_topics and training_record["topic"] not in topic_set and training_record["id"] not in id_set:
                            training_record["test-id"] = test_record["id"]
                            samples.append(training_record)
                            id_set.add(training_record["id"])
                            topic_set.add(training_record["topic"])
                        elif not exists_enough_topics and training_record["id"] not in id_set:
                            training_record["test-id"] = test_record["id"]
                            samples.append(training_record)
                            id_set.add(training_record["id"])
                            topic_set.add(training_record["topic"])
                        if len(samples) == k:
                            all_samples.extend(samples)
                            break
                    if len(samples) < k:
                        exists_enough_topics = False

    else:
        for _, test_record in dataset["test"].iterrows():
            instances_scores_map = similarities[test_record["id"]]
            instances_scores = list(zip(instances_scores_map.keys(), instances_scores_map.values()))
            instances_scores.sort(key = lambda x: x[1], reverse=True)
            for k in ks:
                top_indices, top_scores = zip(*instances_scores[:k])
                samples = df_training[df_training["id"].isin(top_indices)]
                samples.drop_duplicates(["id"], inplace=True) # in perspectrum dataset some entries are duplicate
                #print(test_record["id"])
                samples["test-id"] = test_record["id"]
                samples["score"]=top_scores
                samples["k"]=k
                all_samples.append(samples)
    df_samples = pd.concat(all_samples)
    if different_topics:
        path_samples = f"/bigwork/nhwpajjy/contrastive_learning/sampling_strategies_optimized/{experiment}-most-similar-different-topics-unblanced-contrastive.tsv"
    else:
        path_samples = f"/bigwork/nhwpajjy/contrastive_learning/sampling_strategies_optimized/{experiment}-most-similar-contrastive.tsv"
    df_samples.to_csv(path_samples, sep="\t", encoding="utf-8", columns=["topic", "stance", "text", "id", "score", "test-id", "k"])

