from urllib.parse import quote, urlparse
from app.config import AFFILIATE_TEMPLATE

def extract_product_id(permalink: str) -> str:
    """
    Extrai o ID ou slug do produto a partir do permalink.
    Exemplo:
      https://produto.mercadolivre.com.br/MLB-123456789-smartphone
    vira:
      MLB-123456789-smartphone
    """
    path = urlparse(permalink).path
    return path.strip("/").split("/")[-1]

def make_affiliate_link(permalink: str) -> str:
    product_id = extract_product_id(permalink)
    return AFFILIATE_TEMPLATE.replace("{permalink}", quote(product_id, safe=""))
