import pandas as pd
import json

VALID_CDS = ["1942", "1965", "930", "409", "1953", "1974", "1979", "7801"]

def clean_col_name(name):
    return str(name).strip()

def get_data(sheet_name):
    df = pd.read_excel('/home/ubuntu/upload/basessss.xlsx', sheet_name=sheet_name, header=4)
    df.columns = [clean_col_name(c) for c in df.columns]
    
    cd_col = 'CD' if 'CD' in df.columns else df.columns[0]
    id_col = 'ID' if 'ID' in df.columns else df.columns[1]
    elegivel_col = 'Elegível ao Piloto?'
    
    id_to_cd = {}
    id_to_elegible = {}
    for _, row in df.iterrows():
        uid = row[id_col]
        if pd.isna(uid): continue
        cd = str(row[cd_col]).split('.')[0]
        if cd in VALID_CDS:
            id_to_cd[uid] = cd
            id_to_elegible[uid] = row[elegivel_col] == 'ELEGÍVEL'

    try:
        cad_idx = df.columns.tolist().index('Cadastro.1')
    except ValueError:
        cad_idx = [i for i, c in enumerate(df.columns) if 'Cadastro.1' in c][0]
    
    right_df = df.iloc[:, cad_idx:cad_idx+10].dropna(subset=[df.columns[cad_idx+1]])
    right_df.columns = [clean_col_name(c) for c in right_df.columns]
    
    val_col = [c for c in right_df.columns if 'Valor Líquido R$' in c][0]
    prod_col = [c for c in right_df.columns if 'Bruto Produtividade' in c][0]
    
    cont_list = []
    for _, row in right_df[right_df[val_col] > 0].iterrows():
        mat = row['Cadastro.1']
        if mat in id_to_cd:
            cont_list.append({
                'Matrícula': int(mat),
                'Nome': row['COLABORADOR.1'],
                'Produção': row[prod_col],
                'Valor': row[val_col],
                'CD': id_to_cd[mat]
            })
    
    return id_to_cd, id_to_elegible, cont_list

id_to_cd1, id_to_el1, cont1 = get_data('Piloto Incentivo (2)')
id_to_cd2, id_to_el2, cont2 = get_data('Piloto Incentivo')

all_ids = set(id_to_cd1.keys()).union(set(id_to_cd2.keys()))
cd_metrics = {cd: {"quadro": 0, "elegiveis": 0, "contemplados": 0, "total_pago": 0.0} for cd in VALID_CDS}

for uid in all_ids:
    cd = id_to_cd1.get(uid) or id_to_cd2.get(uid)
    is_el = id_to_el1.get(uid) or id_to_el2.get(uid)
    if cd in cd_metrics:
        cd_metrics[cd]["quadro"] += 1
        if is_el:
            cd_metrics[cd]["elegiveis"] += 1

final_cont = {}
for c in cont1 + cont2:
    mat = c['Matrícula']
    if mat not in final_cont:
        final_cont[mat] = c
    else:
        final_cont[mat]['Produção'] += c['Produção']
        final_cont[mat]['Valor'] += c['Valor']

for mat, data in final_cont.items():
    cd = data['CD']
    if cd in cd_metrics:
        cd_metrics[cd]["contemplados"] += 1
        cd_metrics[cd]["total_pago"] += data['Valor']

top_10 = list(final_cont.values())
top_10.sort(key=lambda x: x['Valor'], reverse=True)
top_10 = top_10[:10]

res = {"by_cd": cd_metrics, "top_10": top_10}
with open('final_data_by_cd_v2.json', 'w') as f:
    json.dump(res, f, indent=4)
print(json.dumps(cd_metrics, indent=4))
