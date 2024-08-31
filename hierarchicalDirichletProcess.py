import re

from gensim import corpora
from gensim.models import HdpModel

def remove_duplicates_2d_list(lst):
    # Step 1: Flatten the 2D list to a 1D list
    flat_list = [item for sublist in lst for item in sublist]

    # Step 2: Remove duplicates while preserving order
    seen = set()
    unique_list = []
    for item in flat_list:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)

    # Step 3: Reconstruct the 2D list while maintaining original sublist sizes
    result = []
    index = 0
    for sublist in lst:
        new_sublist = []
        for _ in sublist:
            if index < len(unique_list):
                new_sublist.append(unique_list[index])
                index += 1
        result.append(new_sublist)
    return [sublist for sublist in result if sublist]


def hdpProcess(S_1, O_3, splitI):
    # 创建词典和语料库
    texts = []
    for i in range(3):
        texts.append(S_1)
    texts.append(O_3)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # 创建HDP模型
    hdp_model = HdpModel(corpus=corpus, id2word=dictionary)

    # 获取所有主题
    topics = hdp_model.show_topics(formatted=True)

    topicsUp = []
    topicsDown = []
    for topicI in topics:
        words = re.findall(r'\b[a-zA-Z]+\b', topicI[1])
        topicsUp.append(words[:splitI])
        topicsDown.append(words[splitI:])

    return remove_duplicates_2d_list(topicsUp),remove_duplicates_2d_list(topicsDown)

