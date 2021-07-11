torch-model-archiver --model-name chatter-kogpt2 --version 1.0 --model-file Language_Model/model.py --serialized-file Language_Model/kogpt2-wellnesee-auto-regressive1.pth --handler torch_handler/api_handler.py
mv chatter-kogpt2.mar /home/model-server/model-store
