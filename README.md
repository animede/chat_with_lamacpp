# chat_with_lamacpp

##使い方

### OpenAI互換サーバを起動

lama.cppをgitからクローン

CPU版またはGPU版を構築

モデルをHuggingFaceからダウンロードし、modelsフォルダーに移動させておく

以下でサーバを起動

./llama-server -m ./models/gemma-2-9b-it-Q4_K_M.gguf -n 2048 --n_gpu_layers 43

### アプリの動かし方

このリポジトリをクローンするか、openai_gui.py　と　index.htmlを所定のフォルダにダウンロードする。

openai_gui.pyで必要なモジュルーは

Fastapi　と　opensi　のみです。

openai_gui.py起動後に表示されるurlにブラウザーでアクセスすればアプリが使えます。

gemma-2-9b-it-Q4_K_M.gguf 
gemma-2-27b-it-Q4_K_M.gguf

での動作を確認しています。
