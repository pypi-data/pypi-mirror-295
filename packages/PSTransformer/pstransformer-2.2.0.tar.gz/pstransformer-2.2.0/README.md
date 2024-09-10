# This is Transformer 
- Sentence translation transformers are advanced models in natural language processing (NLP) that encode entire sentences into high-dimensional vectors, preserving their contextual meaning. These models, such as BERT, RoBERTa, and XLM-RoBERTa, are fine-tuned to generate embeddings that can be used for various tasks like semantic search, clustering, and sentence similarity³. By training on parallel sentences in multiple languages, these transformers can align the vector spaces of different languages, enabling accurate and meaningful translations¹². This approach significantly enhances the performance of NLP applications, making them more effective in multilingual contexts³.


![alt text](Image/full_picture_of_transformer.png)

EXample:  
    
    Ram Eats mango    --> English 

     राम आम खाता  है    --> Hindi


- How to Install this 
```
pip install PSTransformer==<version>

            OR

pip install PSTransformer
```


- if you are import the model of the Transformer then used to this import 
```
# import the transformer model 
>>> from PSTansformer.model import build_transformer

# how to used this transformer model 
>>> build_transformer(
        vocab_src_len=vocabulary_source_length,   # vocabulary source length of sentence like tokeinzer source length of 
        vocab_tgt_len=vocabulary_target_length,    # same for the target language 
        src_seq_len=config["seq_len"],     # source language  length of you sentence like 350 
        tgt_seq_len=config['seq_len'],     # target language length of you sentence same as source length
        d_model=config['d_model']        # dimension model your language like 512
)
```




- if you import the Tensor dataset function, which is convert the tensor data from raw data 
```
# import the Tensor dataset Function
>>> from PSTansformer.dataset import BilingualDataset

# how to used this Tensor dataset which is convert to the Tensor of the row data 
>>> BilingualDataset(
        ds=train_dataset_raw,   # raw dataset like='Ram eats mango'
        tokenizer_src=tokenizer_source,  # source language tokenizer 
        tokenizer_tgt=tokinzer_target,   # target language tokenizer
        src_lang=config['lang_src'],      # source language like engish
        tgt_lang=config['lang_tgt'],     # target language like Hindi
        seq_len=config['seq_len'])      # sequence length like 350
```

- how to used the train model 
```
def get_config():
    return {
        "batch_size": 8,
        "num_epochs": 20,
        "lr": 10**-4,
        "seq_len": 350,
        "d_model": 512,
        "datasource": 'opus_books',
        "lang_src": "en",
        "lang_tgt": "it",
        "model_folder": "weights",
        "model_basename": "tmodel_",
        "preload": "latest",
        "tokenizer_file": "tokenizer_{0}.json",
        "experiment_name": "runs/tmodel"
    }
```

```
    config = get_config()
    train_model(config)
```
# Licence 
[MIT Licence](https://github.com/ProgramerSalar/PSTransformer/blob/master/LICENSE)

# Dependencies 
- ```torch``` 
- ```tqdm ``` this is progress bar library
- ```datasets ```  this is dataset libarary by huggingface
- ```tokenizers ```  this is tokenizers libary by huggingface
- ```tensorboard ```  TensorBoard is a visualization toolkit for machine learning experimentation. TensorBoard allows tracking and visualizing metrics such as loss and accuracy, visualizing the model graph, viewing histograms, displaying images and much more. In this tutorial we are going to cover TensorBoard installation, basic usage with PyTorch, and how to visualize data you logged in TensorBoard UI.


# Uninstall
Uninstall package and dependent package with ```pip``` command .
```
pip uninstall PSTransformer torch tqdm datasets tokenizers tensorboard
```

# Contibuting 
See [contribution guidelines](https://github.com/ProgramerSalar/PSTransformer/blob/master/CONTRIBUTING.md) .


# CHANGELOG

## 1.0.0

- First Implemention version
    - Add a function 

        - ```BilingualDataset()```
        - ```build_transformer()```


## 2.0.0
- solve some Error, I will Get the package error 

## 2.1.0 
- First Stable relased version

   

## 2.2.0
- Improve document
    - Update the README document
    - Add the Licence 
    - some Required Things 


