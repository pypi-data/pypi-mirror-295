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


def generate_similarity_matrix(experiment):
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
    for test_record in tqdm(dataset["test"].iterrows()):
        for train_record in dataset["training"].iterrows():
            similarities[test_record["id"]][train_record["id"]] = float(cosine_scores[i,j])
            j = j + 1
        i = i + 1
        j = 0
    with open(path_similarities, "w") as file:
        json.dump(similarities, file )


def generate_most_similar_stance_arguments(experiment):
    pass

def generate_most_similar_stance_arguments_different_topics(experiment):
    pass

