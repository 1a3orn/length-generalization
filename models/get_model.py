
from models.trans import Transformer
from models.karpathy_trans import GPT as KarpathyTransformer
from models.karpathy_trans_alibi import GPT as KarpathyTransformerAlibi
from models.karpathy_trans_rot import GPT as KarpathyTransformerRot
from models.rwkv.model import RWKV

class KarpSm:
    block_size: int = 0
    vocab_size: int = 0
    n_layer: int = 1
    n_head: int = 4
    n_embd: int = 1 * 256
    bias: bool = True # True: bias in Linears and LayerNorms, like GPT-2. False: a bit better and faster

class KarpMd:
    block_size: int = 0
    vocab_size: int = 0
    n_layer: int = 2
    n_head: int = 4
    n_embd: int = 1 * 256
    bias: bool = True

class KarpLg:
    block_size: int = 0
    vocab_size: int = 0
    n_layer: int = 3
    n_head: int = 4
    n_embd: int = 1 * 256
    bias: bool = True 

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
    if config['model_name'] == "trans_karp_sm":
        KarpSm.block_size = config['ctx_len']
        KarpSm.vocab_size = config['vocab_size']
        return KarpathyTransformer(KarpSm)
    if config['model_name'] == "trans_karp_md":
        KarpMd.block_size = config['ctx_len']
        KarpMd.vocab_size = config['vocab_size']
        return KarpathyTransformer(KarpMd)
    if config['model_name'] == "trans_karp_lg":
        KarpMd.block_size = config['ctx_len']
        KarpMd.vocab_size = config['vocab_size']
        return KarpathyTransformer(KarpLg)
    if config['model_name'] == 'trans_karp_sm_rot':
        KarpSm.block_size = config['ctx_len']
        KarpSm.vocab_size = config['vocab_size']
        return KarpathyTransformerRot(KarpSm)
    if config['model_name'] == 'trans_karp_md_rot':
        KarpMd.block_size = config['ctx_len']
        KarpMd.vocab_size = config['vocab_size']
        return KarpathyTransformerRot(KarpMd)
    if config['model_name'] == 'trans_karp_lg_rot':
        KarpMd.block_size = config['ctx_len']
        KarpMd.vocab_size = config['vocab_size']
        return KarpathyTransformerRot(KarpLg)
    if config['model_name'] == "rwkv_sm":
        class RWKVSm:
            ctx_len: int = config['ctx_len']
            vocab_size: int = config['vocab_size']
            n_layer: int = 1
            n_embd: int = 256
            dropout: float = 0.0
            n_head: int = 4
            bias: bool = True
        return RWKV(RWKVSm)
    if config['model_name'] == "rwkv_md":
        class RWKVMd:
            ctx_len: int = config['ctx_len']
            vocab_size: int = config['vocab_size']
            n_layer: int = 2
            n_embd: int = 256
            dropout: float = 0.0
            n_head: int = 4
            bias: bool = True
        return RWKV(RWKVMd)
    if config['model_name'] == "rwkv_lg":
        class RWKVLg:
            ctx_len: int = config['ctx_len']
            vocab_size: int = config['vocab_size']
            n_layer: int = 3
            n_embd: int = 256
            dropout: float = 0.0
            n_head: int = 4
            bias: bool = True
        return RWKV(RWKVLg)

    else:
        raise ValueError(f"Unknown model: {config['model_name']}")