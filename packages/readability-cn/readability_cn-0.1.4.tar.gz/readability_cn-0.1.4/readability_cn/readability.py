#!python
# author: rao.chenlin@gmail.com
# inspired by <https://github.com/Rebilly/lexi>, using the following formulas:
## Flesch Reading Ease：206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
## Gunning Fog：0.4 * (words/sentences + 100 * (complex words / words))
## Automated Readability Index (ARI)：4.71 * (characters/words) + 0.5 * (words/sentences) - 21.43
## Dale Chall Readability Score：0.1579 * (100 * difficult words / words) + 0.0496 * (words / sentences)
## Coleman Liau Index：0.0588 * (characters/words) - 0.296 * (sentences/words) - 15.8
# 参考文献
# [1]张文雅.基于可读性的信息检索模型研究[D].天津大学,2016.
# [2]曹颖淑.基于NLP技术的企业信息披露质量的评价方法研究[D].上海师范大学,2018.DOI:10.27312/d.cnki.gshsu.2018.000061.
# [3]雷蕾,韦瑶瑜,刘康龙.AlphaReadabilityChinese：汉语文本可读性工具开发与应用[J].外语与外语教学,2024,(01):83-93+149.DOI:10.13458/j.cnki.flatt.004997.
# [4]程勇,徐德宽,董军.基于语文教材语料库的文本阅读难度分级关键因素分析与易读性公式研究[J].语言文字应用,2020,(01):132-143.DOI:10.16499/j.cnki.1003-5397.2020.01.014.
# [5]徐巍,姚振晔,陈冬华.中文年报可读性：衡量与检验[J].会计研究,2021(03):28-44.
# 采用LTP库实现分词、词性识别、主谓宾句法依存识别
# 词性标注集
# -----------
# +-----+---------------------+------------+-----+-------------------+------------+
# | Tag |     Description     |  Example   | Tag |    Description    |  Example   |
# +=====+=====================+============+=====+===================+============+
# | a   |  形容词              | 美丽       | ni  |  组织名称           | 保险公司   |
# +-----+---------------------+------------+-----+-------------------+------------+
# | b   |  其他名词修饰语       | 大型, 西式 | nl  | 位置名词             | 城郊       |
# +-----+---------------------+------------+-----+-------------------+------------+
# | c   |  连词                | 和, 虽然   | ns  | 地理名称            | 北京       |
# +-----+---------------------+------------+-----+-------------------+------------+
# | d   |  副词                | 很         | nt  |  时间名词          | 近日, 明代 |
# +-----+---------------------+------------+-----+-------------------+------------+
# | e   |  叹词                | 哎         | nz  |  其他专有名词       | 诺贝尔奖   |
# +-----+---------------------+------------+-----+-------------------+------------+
# | g   |  词素                | 茨, 甥     | o   |  拟声词            | 哗啦       |
# +-----+---------------------+------------+-----+-------------------+------------+
# | h   |  前缀                | 阿, 伪     | p   | 介词               | 在, 把     |
# +-----+---------------------+------------+-----+-------------------+------------+
# | i   |  成语                | 百花齐放   | q   | 数量                | 个         |
# +-----+---------------------+------------+-----+-------------------+------------+
# | j   |  缩写                | 公检法     | r   | 代词                | 我们       |
# +-----+---------------------+------------+-----+-------------------+------------+
# | k   |  后缀                | 界, 率     | u   | 辅助词             | 的, 地     |
# +-----+---------------------+------------+-----+-------------------+------------+
# | m   |  数字                | 一, 第一   | v   |  动词              | 跑, 学习   |
# +-----+---------------------+------------+-----+-------------------+------------+
# | n   |  通用名词             | 苹果       | wp  | 标点符号            | ，。！     |
# +-----+---------------------+------------+-----+-------------------+------------+
# | nd  |  方向名词             | 右侧       | ws  | 外语               | CPU        |
# +-----+---------------------+------------+-----+-------------------+------------+
# | nh  |  人名                | 杜甫, 汤姆 | x   |  非词素             | 萄, 翱     |
# +-----+---------------------+------------+-----+-------------------+------------+
# |     |                     |            | z   | 描述性词语          | 瑟瑟，匆匆 |
# +-----+---------------------+------------+-----+-------------------+------------+
# 
# 依存句法关系
# ---------------------
# +------------+-----+---------------------------+----------------------------+
# |  关系类型  | Tag |        Description        |          Example           |
# +============+=====+===========================+============================+
# | 主谓关系   | SBV | subject-verb              | 我送她一束花 (我 <-- 送)   |
# +------------+-----+---------------------------+----------------------------+
# | 动宾关系   | VOB | 直接宾语，verb-object     | 我送她一束花 (送 --> 花)   |
# +------------+-----+---------------------------+----------------------------+
# | 间宾关系   | IOB | 间接宾语，indirect-object | 我送她一束花 (送 --> 她)   |
# +------------+-----+---------------------------+----------------------------+
# | 前置宾语   | FOB | 前置宾语，fronting-object | 他什么书都读 (书 <-- 读)   |
# +------------+-----+---------------------------+----------------------------+
# | 兼语       | DBL | double                    | 他请我吃饭 (请 --> 我)     |
# +------------+-----+---------------------------+----------------------------+
# | 定中关系   | ATT | attribute                 | 红苹果 (红 <-- 苹果)       |
# +------------+-----+---------------------------+----------------------------+
# | 状中结构   | ADV | adverbial                 | 非常美丽 (非常 <-- 美丽)   |
# +------------+-----+---------------------------+----------------------------+
# | 动补结构   | CMP | complement                | 做完了作业 (做 --> 完)     |
# +------------+-----+---------------------------+----------------------------+
# | 并列关系   | COO | coordinate                | 大山和大海 (大山 --> 大海) |
# +------------+-----+---------------------------+----------------------------+
# | 介宾关系   | POB | preposition-object        | 在贸易区内 (在 --> 内)     |
# +------------+-----+---------------------------+----------------------------+
# | 左附加关系 | LAD | left adjunct              | 大山和大海 (和 <-- 大海)   |
# +------------+-----+---------------------------+----------------------------+
# | 右附加关系 | RAD | right adjunct             | 孩子们 (孩子 --> 们)       |
# +------------+-----+---------------------------+----------------------------+
# | 独立结构   | IS  | independent structure     | 两个单句在结构上彼此独立   |
# +------------+-----+---------------------------+----------------------------+
# | 核心关系   | HED | head                      | 指整个句子的核心           |
# +------------+-----+---------------------------+----------------------------+

import re
import os
import sys
import numpy as np
import torch
from ltp import LTP, StnSplit

class ChineseReadability:
    def __init__(self, model_path="LTP/small", use_gpu=True):
        self.ltp = LTP(model_path)
        self.stnsplit = StnSplit()

        if use_gpu and torch.cuda.is_available():
            self.ltp.to("cuda")

        self.hsk3_vocab = self._load_hsk3_vocab()
        self.stroke_counts = self._load_stroke_counts()
        self.jia_chars = self._load_jia_chars()
        self.jia_words = self._load_jia_words()
        self.char_freq = self._load_char_freq()

    def add_custom_words(self, words, freq=2):
        """
        Add custom words to the LTP tokenizer.
        
        :param words: A list of words or a dictionary of words with their frequencies.
        :param freq: Default frequency for words if a list is provided.
        """
        if isinstance(words, list):
            words_dict = {word: freq for word in words}
        elif isinstance(words, dict):
            words_dict = words
        else:
            raise ValueError("Words should be a list or a dictionary.")

        for word, freq in words_dict.items():
            self.ltp.add_words([word], freq=freq)

    def _load_hsk3_vocab(self):
        with open(os.path.join(os.path.dirname(__file__), 'data/hsk3_vocabulary.txt'), 'r', encoding='utf-8') as f:
            return set(f.read().split())

    def _load_stroke_counts(self):
        stroke_counts = {}
        with open(os.path.join(os.path.dirname(__file__), 'data/zi-dataset.tsv'), 'r', encoding='utf-8') as f:
            next(f)  # Skip the header line
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) >= 2:
                    character = fields[0]
                    stroke_count = int(fields[1].rstrip('画'))
                    stroke_counts[character] = stroke_count
        return stroke_counts

    def _load_jia_chars(self):
        with open(os.path.join(os.path.dirname(__file__), 'data/hanzi_jia.txt'), 'r', encoding='utf-8') as f:
            return set(f.read().strip())

    def _load_jia_words(self):
        with open(os.path.join(os.path.dirname(__file__), 'data/ci_jia.txt'), 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())

    def _load_custom_vocab(self, vocab_file_path=os.path.join(os.path.dirname(__file__), 'data/filtered_computer.vocab')):
        with open(vocab_file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            custom_vocab = set(line.split('\t')[0] for line in lines[:int(len(lines) * 0.16)])
            self.jia_words.update(custom_vocab)

    def _load_char_freq(self):
        char_freq = {}
        with open(os.path.join(os.path.dirname(__file__), 'data/character_frequency.csv'), 'r', encoding='utf-8') as f:
            next(f)  # Skip header
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    char = parts[1]
                    freq = float(parts[3])
                    char_freq[char] = freq
        return char_freq

    def _convert_asciidoc_tables_to_text(self, content: str) -> str:
        def process_table(match):
            table_content = match.group(1)
            rows = table_content.strip().split('\n')
            processed_rows = []
            for row in rows:
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                processed_rows.append('. '.join(cells))
            return '\n'.join(processed_rows)
        return re.sub(r'\|===\n([\s\S]*?)\|===', process_table, content)

    def _convert_markdown_tables_to_text(self, content: str) -> str:
        def process_table(match):
            table_content = match.group(1)
            rows = table_content.strip().split('\n')
            header = rows[0]
            separator = rows[1]
            data_rows = rows[2:]
            
            # Extract column names
            columns = [col.strip() for col in header.split('|') if col.strip()]
            
            # Process data rows
            processed_rows = []
            for row in data_rows:
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                if len(cells) == len(columns):
                    processed_row = '. '.join(f"{col}: {cell}" for col, cell in zip(columns, cells))
                    processed_rows.append(processed_row)
            
            return '\n'.join(processed_rows)

        # Find and replace all markdown tables
        pattern = r'\n\|.*\|.*\n\|[-:| ]+\|\n((?:\|.*\|.*\n)+)'
        return re.sub(pattern, lambda m: '\n' + process_table(m) + '\n', content)

    def preprocess_asciidoc(self, content: str) -> str:
        # Convert tables to text
        content = self._convert_asciidoc_tables_to_text(content)
        # Remove frontmatter
        content = re.sub(r'^---\n[\s\S]*?\n---\n', '', content)
        # Remove horizontal rules
        content = re.sub(r'^-{3,}$', '', content, flags=re.MULTILINE)
        # Remove images, code blocks, and HTML
        content = re.sub(r'image:.*?(\[.*?\])?', '', content)
        content = re.sub(r'----\n[\s\S]*?----', '', content)
        content = re.sub(r'<.*?>', '', content)
        # Remove headers
        content = re.sub(r'^=+\s.*$', '', content, flags=re.MULTILINE)
        # Remove URL links
        content = re.sub(r'https?://\S+', '', content)
        content = re.sub(r'\b\w+://\S+', '', content)
        # Convert colons to periods in headings
        content = re.sub(r'^(=+)\s*(.+):(.*)$', r'\1 \2.\3', content, flags=re.MULTILINE)
        # Add periods to list items if they don't already have punctuation
        content = re.sub(r'^(\*+|\d+\.)\s+([^.\n]+)(?<![.!?])$', r'\1 \2。', content, flags=re.MULTILINE)
        # Remove short list items (less than 5 characters)
        content = re.sub(r'^(\*+|\d+\.)\s+.{1,4}$\n', '', content, flags=re.MULTILINE)
        # Remove all code blocks
        content = re.sub(r'----\n\[source,[^\]]+\][\s\S]*?----', '', content)
        # Remove asciidoc tags
        content = re.sub(r'\[.*?\]', '', content)  # Remove attribute lists
        content = re.sub(r'^:.*?:.*$', '', content, flags=re.MULTILINE)  # Remove attribute entries
        content = re.sub(r'ifdef::.*?endif::', '', content, flags=re.DOTALL)  # Remove conditional processing
        content = re.sub(r'include::.*?\[]', '', content)  # Remove include directives
        # Remove any blank lines
        content = re.sub(r'\n+', '\n', content)
        # Remove any new lines that are added for manual word wrapping
        content = re.sub(r'([a-zA-Z])\n', r'\1 ', content)    
        return content.strip()

    def preprocess_markdown(self, content: str) -> str:
        # Convert tables to text
        content = self._convert_markdown_tables_to_text(content)
        # Remove frontmatter
        content = re.sub(r'^---\n[\s\S]*?\n---\n', '', content)
        # Remove horizontal rules
        content = re.sub(r'^-{3,}$', '', content, flags=re.MULTILINE)
        # Remove images
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)
        # Remove inline code
        content = re.sub(r'`.*?`', '', content)
        # Remove HTML tags
        content = re.sub(r'<.*?>', '', content)
        # Remove headers
        content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
        # Remove URL links
        content = re.sub(r'\[([^\]]+)\]\(https?://\S+\)', r'\1', content)  # Remove named links
        content = re.sub(r'https?://\S+', '', content)  # Remove bare URLs
        # Convert colons to periods in headings (if any remain)
        content = re.sub(r'^(#+)\s*(.+):(.*)$', r'\1 \2.\3', content, flags=re.MULTILINE)
        # Add periods to list items if they don't already have punctuation
        content = re.sub(r'^(\*|-|\d+\.)\s+([^.\n]+)(?<![.!?])$', r'\1 \2。', content, flags=re.MULTILINE)
        # Remove short list items (less than 5 characters)
        content = re.sub(r'^(\*|-|\d+\.)\s+.{1,4}$\n', '', content, flags=re.MULTILINE)
        # Remove any blank lines
        content = re.sub(r'\n+', '\n', content)
        # Remove any new lines that are added for manual word wrapping
        content = re.sub(r'([a-zA-Z])\n', r'\1 ', content)
        return content.strip()

    def preprocess_html(self, content: str) -> str:
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Remove scripts
        content = re.sub(r'<script[\s\S]*?</script>', '', content)
        # Remove styles
        content = re.sub(r'<style[\s\S]*?</style>', '', content)
        # Remove comments
        content = re.sub(r'<!--[\s\S]*?-->', '', content)
        # Convert entities to characters
        content = html.unescape(content)
        # Remove multiple spaces
        content = re.sub(r'\s+', ' ', content)
        # Remove URLs
        content = re.sub(r'https?://\S+', '', content)
        # Add periods to list items if they don't already have punctuation
        content = re.sub(r'(•|\*|-|\d+\.)\s+([^.\n]+)(?<![.!?])$', r'\1 \2。', content, flags=re.MULTILINE)
        # Remove short list items (less than 5 characters)
        content = re.sub(r'(•|\*|-|\d+\.)\s+.{1,4}$\n', '', content, flags=re.MULTILINE)
        # Remove any blank lines
        content = re.sub(r'\n+', '\n', content)
        # Remove any new lines that are added for manual word wrapping
        content = re.sub(r'([a-zA-Z])\n', r'\1 ', content)
        return content.strip()

    ## 程勇难度指标 = 38.36 - 45.65 * 平均字频(邢红兵25亿字语料字频表) + 54.92 * 连词比例 - 8.96 * 物词义类比例 + 11.13 * 词义丰富度 - 12.34 * 动作词义类比例 + 0.012 * 句长变化度 + 20 * 关联词义类比例
    ## 取值范围: [15, 140]
    ## 假设句长变化度最大值为 1000，字频最大值为 15000
    def chengyong_readability(self, sentences):
        # Calculate sentence length variance
        sentence_lengths = [len(sent) for sent in sentences]
        sentence_length_variance = np.var(sentence_lengths) if sentence_lengths else 0
    
        # Process the sentences
        words = []
        pos_tags = []
        deps = []
        total_freq = 0
        char_count = 0
        
        for sent in sentences:
            output = self.ltp.pipeline(sent, tasks=["cws", "pos", "dep"])
            words.extend(output.cws)
            pos_tags.extend(output.pos)
            deps.extend(output.dep)
            
            # Calculate average character frequency
            for char in sent:
                if char in self.char_freq:
                    total_freq += self.char_freq[char]
                    char_count += 1
        
        avg_char_freq = total_freq / char_count if char_count > 0 else 0
        
        total_words = len(words)
        
        # Map LTP POS tags to Cilin categories
        cilin_categories = {
            'human': ['nh'],
            'object': ['n', 'ni', 'nl', 'ns', 'nt', 'nz'],
            'time_space': ['nd', 'nt'],
            'abstract': ['a', 'b', 'i', 'j', 'z'],
            'feature': ['a', 'b', 'd'],
            'action': ['v', 'vn'],
            'mental': ['v', 'a'],  # Simplified, might need refinement
            'activity': ['v', 'vn'],
            'phenomenon_state': ['a', 'v'],
            'relation': ['c', 'p'],
            'auxiliary': ['u', 'k', 'h'],
            'respectful': []  # LTP doesn't have a specific tag for this
        }
    
        # Categorize words and count
        category_counts = {cat: 0 for cat in cilin_categories}
        for word, pos in zip(words, pos_tags):
            for category, pos_list in cilin_categories.items():
                if pos in pos_list:
                    category_counts[category] += 1
                    break
    
        # Calculate category ratios
        category_ratios = {cat: count / total_words if total_words > 0 else 0 
                           for cat, count in category_counts.items()}
    
        # Calculate semantic richness (number of non-zero categories / total categories)
        semantic_richness = sum(1 for count in category_counts.values() if count > 0) / len(category_counts)
    
        # Update readability formula
        readability = (38.36 - 45.65 * avg_char_freq / 1000000 + 
                       54.92 * category_ratios['relation'] - 
                       8.96 * category_ratios['object'] + 
                       11.13 * semantic_richness - 
                       12.34 * category_ratios['action'] + 
                       0.012 * sentence_length_variance + 
                       20 * category_ratios['relation'])
        return readability
    
    ## 徐巍可读性指标 = 0.5 * (每个分句的平均字数 + 每个句子中副词和连词的比例)
    ## 这个指标过于简单，几乎就取决于你逗号用得多不多
    def xuwei_readability(self, sentences):
        zi_num_per_clause = []
        adv_conj_ratio_per_sent = []
        for sent in sentences:
            clauses = re.split('[，；：]', sent)
            for clause in clauses:
                zi_num_per_clause.append(len(clause))
            
            words = self.ltp.pipeline(sent, tasks=["cws", "pos"])
            total_words = len(words.cws)
            adv_conj_num = sum(1 for pos in words.pos if pos in ['c', 'd'])
            adv_conj_ratio = adv_conj_num / total_words if total_words > 0 else 0
            adv_conj_ratio_per_sent.append(adv_conj_ratio)
        
        avg_zi_num = np.mean(zi_num_per_clause)
        avg_adv_conj_ratio = np.mean(adv_conj_ratio_per_sent)
        readability = (avg_zi_num + avg_adv_conj_ratio) * 0.5
        return readability
    
    ## 孙汉银中学生阅读难度指标 = -11.848 + 2.135 * 平均笔画数 + 0.15 * 句均字数 + 7.117 * 非hsk三级词比例 + 0.164 * 句均词数
    ## 取值范围: [-8.5, 63]
    ## 假设一般情况下，汉字笔画数在 1-30 之间，句子长度在 5-50 个字之间，3-20 个词之间
    def sunhanyin_readability(self, sentences):
        total_strokes = 0
        total_chars = 0
        total_words = 0
        non_hsk3_words = 0
        for sent in sentences:
            words = self.ltp.pipeline(sent, tasks=["cws"]).cws
            total_words += len(words)
            
            for word in words:
                if word not in self.hsk3_vocab:
                    non_hsk3_words += 1
            
            for char in sent:
                if char in self.stroke_counts:
                    total_strokes += self.stroke_counts[char]
                    total_chars += 1
        
        avg_strokes = total_strokes / total_chars if total_chars > 0 else 0
        avg_words_per_sentence = total_words / len(sentences) if sentences else 0
        non_hsk3_ratio = non_hsk3_words / total_words if total_words > 0 else 0
        readability = -11.848 + 2.135 * avg_strokes + 0.15 * (total_chars / len(sentences)) + 7.117 * non_hsk3_ratio + 0.164 * avg_words_per_sentence
        return readability
    
    ## 王蕾日韩留学生汉语可读性指标 = 72.749 - 7.515 * 虚词(介词、连词、助词、叹词)数 + 0.802 * 简单词数 - 0.462 * 总词数 + 2.446 * 分句数
    ## 注意：虚词里没算副词，分句包括逗号冒号，因此这个公式的计算结果抖动较大。
    def wanglei_readability(self, sentences):
        # Count variables
        function_words = set()
        simple_words = set()
        total_words = set()
        sentence_count = len(sentences)
        
        # Function word POS tags
        function_word_tags = set(['p', 'c', 'u', 'e'])
    
        # Process each sentence
        for sent in sentences:
            # Count sub-sentences based on commas, semicolons, and colons
            sub_sentence_count = sent.count('，') + sent.count('；') + sent.count('：')
            sentence_count += sub_sentence_count
            output = self.ltp.pipeline(sent, tasks=["cws", "pos"])
            words = output.cws
            pos_tags = output.pos
            total_words.update(words)
            
            for word, pos in zip(words, pos_tags):
                if pos in function_word_tags:
                    function_words.add(word)
                if word in self.jia_words:
                    simple_words.add(word)
        
        # Calculate readability score
        readability = 72.749 - 7.515 * len(function_words) + 0.802 * len(simple_words) - 0.462 * len(total_words) + 2.446 * sentence_count
        return readability
    
    ## 曹颖淑三因素可读性指标 = 14.95961 + 1.11506 * 包含主谓宾的完整句比例 + 39.07746 * 《汉语三级考试》基础词汇比例 - 2.48491 * 平均笔画数
    ## 曹颖淑七因素可读性指标 = 13.90963 + 1.54461 * 包含主谓宾的完整句比例 + 39.01497 * 《汉语三级考试》基础词汇比例 - 2.52206 * 平均笔画数 + 0.29809 * 笔画数为5的字符比例 + 0.36192 * 笔画数为12的字符比例 + 0.99363 * 笔画数为22的字符比例 - 1.64671 * 笔画数为25的字符比例
    ## 取值范围: [-60, 50]
    def caoyinshu_readability(self, sentences):
        total_sentences = len(sentences)
        complete_sentences = 0
        total_strokes = 0
        total_chars = 0
        total_words = 0
        hsk3_words = 0
        stroke_5_count = 0
        stroke_12_count = 0
        stroke_22_count = 0
        stroke_25_count = 0
        
        for sent in sentences:
            # Check for subject-predicate-object structure
            output = self.ltp.pipeline(sent, tasks=["cws", "dep"])
            if any(rel == 'SBV' for rel in output.dep) and any(rel == 'VOB' for rel in output.dep):
                complete_sentences += 1
            total_words += len(output.cws)
            hsk3_words += sum(1 for word in output.cws if word in self.hsk3_vocab)
            # Count strokes and characters
            for char in sent:
                if char in self.stroke_counts:
                    total_strokes += self.stroke_counts[char]
                    total_chars += 1
                    if self.stroke_counts[char] == 5:
                        stroke_5_count += 1
                    elif self.stroke_counts[char] == 12:
                        stroke_12_count += 1
                    elif self.stroke_counts[char] == 22:
                        stroke_22_count += 1
                    elif self.stroke_counts[char] == 25:
                        stroke_25_count += 1
        
        svo_ratio = complete_sentences / total_sentences
        avg_strokes = total_strokes / total_chars if total_chars > 0 else 0
        hsk3_ratio = hsk3_words / total_words if total_words > 0 else 0
        # Calculate three-factor readability
        readability_three = 14.95961 + 1.11506 * svo_ratio + 39.07746 * hsk3_ratio - 2.48491 * avg_strokes
        # Additional calculations for seven-factor readability        
        stroke_5_ratio = stroke_5_count / total_chars if total_chars > 0 else 0
        stroke_12_ratio = stroke_12_count / total_chars if total_chars > 0 else 0
        stroke_22_ratio = stroke_22_count / total_chars if total_chars > 0 else 0
        stroke_25_ratio = stroke_25_count / total_chars if total_chars > 0 else 0
        
        # Calculate seven-factor readability
        readability_seven = (13.90963 + 1.54461 * svo_ratio + 39.01497 * hsk3_ratio - 2.52206 * avg_strokes +
                             0.29809 * stroke_5_ratio + 0.36192 * stroke_12_ratio + 0.99363 * stroke_22_ratio -
                             1.64671 * stroke_25_ratio)
        
        return readability_three, readability_seven
    
    ## 郭望皓对外汉语难度指标 = -11.946 + 0.198 * 汉字难度 + 0.123 * 平均句长 + 0.811 * 词汇难度
    ## 《汉语水平词汇与汉字等级大纲》的甲、乙、丙、丁、超纲字/词数占比；文中加权词汇难度的相关度近似于甲级词占比
    ## 汉字难度 = 0.148A + 0.182B + 0.137C + 0.215D + 0.283E
    ## 词汇难度 = 0.132A + 0.185B + 0.249C + 0.246D + 0.188E
    ## 找不到具体的分级表，暂不实现
    def guowanghao_readability(self, text):
        pass
    
    ## 左虹欧美留学生难度指标 =  23.646 + 0.485 * 汉字水平大纲常用甲级字数 - 125.931 * 非甲乙级词数占比 - 0.647 * 虚词(介词、连词、助词、叹词、副词、方位词)数
    ## 杨金余高级汉语精读教材研究中指出：平均每百字的难字为 3-7 个，平均每百字的难词为 10-20 个，平均每百字的固定成语词组数不超过 2 个，平均每百字的丙级以上句法项目不超过 1 个。全文 1000-3000 字，平均每句 20-40 字。
    ## 则估算的取值范围: [170， 1400]，太离谱了。所以决定参照王蕾指标的算法，将甲级字数和虚词数改成去重值。
    def zuohong_readability(self, sentences):
        total_chars = 0
        unique_jia_chars = set()
        total_words = 0
        non_jia_words_count = 0
        unique_function_words = set()
    
        for sent in sentences:
            # Process each sentence
            output = self.ltp.pipeline(sent, tasks=["cws", "pos"])
            words = output.cws
            pos_tags = output.pos
    
            # Count characters and unique Jia-level characters
            for char in sent:
                total_chars += 1
                if char in self.jia_chars:
                    unique_jia_chars.add(char)
    
            # Count words, non-Jia words, and unique function words
            for word, pos in zip(words, pos_tags):
                total_words += 1
                if word not in self.jia_words:
                    non_jia_words_count += 1
                if pos in ['c', 'p', 'u', 'd', 'e', 'nd']:  # Function word POS tags in LTP
                    unique_function_words.add(word)
    
        # Calculate counts
        jia_chars_count = len(unique_jia_chars)
        function_words_count = len(unique_function_words)
    
        # Calculate ratios
        jia_chars_ratio = jia_chars_count / total_chars if total_chars > 0 else 0
        non_jia_words_ratio = non_jia_words_count / total_words if total_words > 0 else 0
    
        # Calculate Zuohong readability index
        readability = 23.646 + 0.485 * jia_chars_count - 125.931 * non_jia_words_ratio - 0.647 * function_words_count
        return readability

    def process_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if file_name.endswith('.adoc'):
            sample_text = self.preprocess_asciidoc(content)
        elif file_name.endswith('.md'):
            sample_text = self.preprocess_markdown(content)
        else:
            # For other file types, use the content as is
            sample_text = content
        sentences = [sentence.strip() for sentence in self.stnsplit.split(sample_text) if sentence.strip()]
        return sentences

    def _compare_scores(self, old_score, new_score, name, higher_is_simpler):
        diff = new_score - old_score
        change = "简单" if (diff > 0) == higher_is_simpler else "难"
        print(f"{name}可读性指标: {old_score:.2f} -> {new_score:.2f} (变化: {diff:.2f}, 文本变{change})")

    def analyze(self, old_file_name, new_file_name):
        old_sentences = self.process_file(old_file_name)
        new_sentences = self.process_file(new_file_name)

        # 曹颖淑可读性指标
        old_score3, old_score7 = self.caoyinshu_readability(old_sentences)
        new_score3, new_score7 = self.caoyinshu_readability(new_sentences)
        self._compare_scores(old_score3, new_score3, "曹颖淑三因素", True)
        self._compare_scores(old_score7, new_score7, "曹颖淑七因素", True)

        # 孙汉银可读性指标
        old_sunhanyin = self.sunhanyin_readability(old_sentences)
        new_sunhanyin = self.sunhanyin_readability(new_sentences)
        self._compare_scores(old_sunhanyin, new_sunhanyin, "孙汉银", False)

        # 程勇可读性指标
        old_chengyong = self.chengyong_readability(old_sentences)
        new_chengyong = self.chengyong_readability(new_sentences)
        self._compare_scores(old_chengyong, new_chengyong, "程勇", True)

        # 左虹可读性指标
        old_zuohong = self.zuohong_readability(old_sentences)
        new_zuohong = self.zuohong_readability(new_sentences)
        self._compare_scores(old_zuohong, new_zuohong, "左虹", True)


def main():
    if len(sys.argv) < 3:
        print("Usage: readability_cn <old_adoc_file> <new_adoc_file>")
        print("Compare readability scores between two AsciiDoc files.")
        print()
        print("Arguments:")
        print("  old_adoc_file    Path to the original AsciiDoc file")
        print("  new_adoc_file    Path to the modified AsciiDoc file")
        print()
        print("The program will calculate and compare various readability scores")
        print("between the two provided files, showing how the text complexity")
        print("has changed.")
        sys.exit(1)

    old_file_name = sys.argv[1]
    new_file_name = sys.argv[2]

    readability = ChineseReadability()
    readability.analyze(old_file_name, new_file_name)

if __name__ == "__main__":
    main()

