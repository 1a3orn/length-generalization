
from models.trans import Transformer
from models.karpathy_trans import GPT as KarpathyTransformer
from models.karpathy_trans_rot import GPT as KarpathyTransformerRot

class Karp:
    block_size: int = 0
    vocab_size: int = 0
    n_layer: int = -1
    n_head: int = 8
    n_embd: int = 1 * 256
    bias: bool = True # True: bias in Linears and LayerNorms, like GPT-2. False: a bit better and faster

def get_model(config: dict) -> object:
    if config['model_name'] == "trans_sm":
        return Transformer({
            'vocab_size': config['vocab_size'],
            'ctx_len': config['ctx_len'],
            'hidden_dim': 128,
            'num_heads': 8,
            'num_layers': 1,
        })
    if config['model_name'] == "trans_md":
        return Transformer({
            'vocab_size': config['vocab_size'],
            'ctx_len': config['ctx_len'],
            'hidden_dim': 128,
            'num_heads': 8,
            'num_layers': 2,
        })
    
    if config['model_name'].startswith("trans_karp_rot_"):
        Karp.block_size = config['ctx_len']
        Karp.vocab_size = config['vocab_size']
        n_layer = int(config['model_name'].split("_")[-1])
        Karp.n_layer = n_layer
        print("Karp Rot", Karp.n_layer)
        return KarpathyTransformerRot(Karp)

    if config['model_name'].startswith("trans_karp_"):
        Karp.block_size = config['ctx_len']
        Karp.vocab_size = config['vocab_size']
        n_layer = int(config['model_name'].split("_")[-1])
        Karp.n_layer = n_layer
        print("Karp", Karp.n_layer)
        return KarpathyTransformer(Karp)

    else:
        raise ValueError(f"Unknown model: {config['model_name']}")