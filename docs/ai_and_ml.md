# Artificial Intelligence (AI) and Machine Learning (ML) in spam filtering

The `spamfilter` package provides several methods to integrate Artificial Intelligence (AI), more specifically, Machine Learning (ML) into the spam filtering process. This allows for more accurate and modern spam filtering techniques to be used in your pipelines.

However, these do not come without risk; please make sure to have read the following disclaimer before using any of these features.

## Things to consider before integrating AI

Before adding any AI-based spam filtering methods, please consider the following:

- is your project or use case of reasonable scale for the application of these technologies? If your project is rather small and short on budget, compute can become unreasonably expensive.
- can you solve the problem without uselessly integrating AI as a buzzword? You don't need to use AI for everything, and sometimes simpler solutions are more effective, dramatically faster and resource-efficient.
- did you consider the license of the AI model you picked for spam filtering? If you don't have the rights to use the model, you might be violating the license and can be held liable for it.

## How to get started, correctly

Don't just add the `MLTextClassifier` into your pipeline and call it a day. AI models can be...

- big to download, slowing down spin-up time of your application when frequently re-deployed
- expensive to run, especially if you use a large model or a lot of data
- bad for the environment if run for several hundreds of thousand times per day

You can use techniques like making use of the `normal-quick` mode in pipelines to stop evaluation as soon as any filter detects a problem, which would eliminate the need to call any more expensive filters (like the ones using AI).

You should also make sure that the models used in your filters are well-trained, not too large and suitable for the task. The `MLTextClassifier`, for example, uses a model to detect hate speech and may not be suited for detecting spam in emails.

## Available AI-based filters

There are three main filters that you may want to use in order to integrate AI into your spam filtering pipeline:

- `MLTextClassifier`: A text classifier that uses a pre-trained model to classify text as spam or not spam. It is based on the `transformers` library and requires a model to be downloaded.
- `Ollama`: A filter that uses the Ollama API to classify text as spam or not spam. It requires an Ollama server to be running and accessible, is even more expensive than the `MLTextClassifier` and should only be used if you have a good reason to do so, for example, correcting harmful text to non-harmful text.
- `API`: A general-purpose filter you may want to use in order to call third-party APIs to classify text as spam or not spam. This is a very flexible filter that can be used to integrate any API that returns a classification result.
