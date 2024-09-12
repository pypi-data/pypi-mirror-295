import json


def format_response(input_data : dict,result : dict,processed_at : str) -> dict:
    """
    """

    extraction_result : dict = result
    address_result : dict = json.loads((extraction_result['endereco']).replace("'",'"'))

    # 
    reliability : int = int(extraction_result['confiabilidade'])

    trust : bool = True if reliability >= 85 else False

    if trust == True:

        return {
            "transaction":{
                "id": input_data['transaction_id'],
                "client":input_data['response_info']['client'],
                "processed_at":processed_at,
                "reliability": reliability,
                "trust":trust,
                "notes":extraction_result['observacao'],
            },
            "data" : {
                    "providerData": {
                    "name" : extraction_result['nome_distribuidora'],
                    "cnpj": int(extraction_result['resultado_distribuidora'])
                },
                "customer":{
                    "name":extraction_result['titular'],
                    "address": {
                        "streetAndNumber": address_result['rua'],
                        "city": address_result['cidade'],
                        "state": address_result['estado'],
                        "zipCode": address_result['cep'],
                        "district": address_result['bairro'],
                    }
                },
                "dates":{
                    "due":extraction_result['vencimento'], # Ver se vale formatar para datetime
                },
                "locationNumber":extraction_result['uc'],
                "subgroup":(extraction_result['subgrupo']).upper(),
                "totalCharges":float(extraction_result['valor']),
                "tariffModality":(extraction_result['modalidade_tarifaria']).upper(),
                "supply_type" : (extraction_result.get('tipo_fornecimento')).upper(),
                "energy":{
                    "demand":float(extraction_result['demanda']) if extraction_result['demanda'] != "" else None,
                    "peak":float(extraction_result['consumo_ponta']) if extraction_result['consumo_ponta'] != "" else None,
                    "off-peak":float(extraction_result['consumo_fora_ponta']) if extraction_result['consumo_fora_ponta'] != "" else None,
                    "total": float(extraction_result['consumo_total']) if extraction_result.get("consumo_total") != None else None,
                }
            }
        }
    
    return {
         "transaction":{
            "id": input_data['transaction_id'],
            "client":input_data['response_info']['client'],
            "processed_at":processed_at,
            "reliability": reliability,
            "trust":trust,
            "notes":extraction_result['observacao'],
        },
        "data" : {}
    }