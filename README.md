# wordbreak

Some Python code for analyzing text data. Includes two broad steps: word segmentation and topic analysis.

The word segmentation part includes two complementing algorithms: variable length n-gram word frequency counter, which has large memory requirement and runs in one pass;
and dirichlet process based gibbs sampling segmenter, which uses less memory but takes many iterations to converg. 
The static method is used to create initial points for the stochastic method.

The topic analysis part also comes in two flavours. One is PCA to create word embedding and spherical EM clustering on the word vectors. The other one is LDA for grouping words into topics.
I eventually preferred PCA approach as LDA can take a really long time to run.
