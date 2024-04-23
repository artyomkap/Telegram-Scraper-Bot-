import os

from aiocryptopay import AioCryptoPay

async def check_crypto_bot_invoice(invoice_id: int):
    cryptopay = AioCryptoPay(os.getenv('CRYPTO_BOT'))
    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    await cryptopay.close()
    if invoice and invoice.status == 'paid':
        return True
    else:
        return False