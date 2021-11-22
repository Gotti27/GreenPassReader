import json
import zlib
import flynn
import base45

schema = open('schema.json', 'r')
glb_schema = json.load(schema)

expirations = {  # only the main ones in Europe
    "1232": ("test", 2),
    "ORG-100001699": ("AstraZeneca", 180),  # AstraZeneca
    "ORG-100030215": ("BionTech Manufacturing GmbH", 180),  # BionTech Manufacturing GmbH
    "ORG-100031184": ("Moderna", 180),  # Moderna
}


def decode_gpass(gpass_b45):
    gpass_json = []
    # strip header ('HC1:') and decompress data:
    gpass_zlib = base45.b45decode(gpass_b45[4:])
    gpass = zlib.decompress(gpass_zlib)

    # decode cose document:
    (_, (headers1, headers2, cbor_data, signature)) = flynn.decoder.loads(gpass)
    # decode cbor-encoded payload:
    data = flynn.decoder.loads(cbor_data)

    def annotate(gpass_data, gpass_schema, level=0):
        for key, value in gpass_data.items():
            description = gpass_schema[key].get('title') or gpass_schema[key].get('description') or key
            description, _, _ = description.partition(' - ')
            gpass_json.append(value)
            if type(value) is dict:
                _, _, sch_ref = gpass_schema[key]['$ref'].rpartition('/')
                annotate(value, glb_schema['$defs'][sch_ref]['properties'],
                level+1)
            elif type(value) is list:
                _, _, sch_ref = gpass_schema[key]['items']['$ref'].rpartition('/')
                for v in value:
                    annotate(v, glb_schema['$defs'][sch_ref]['properties'], level+1)
            else:  # value is scalar
                pass
        return gpass_json

    decoded = annotate(data[-260][1], glb_schema['properties'])

    if expirations[decoded[2]][0] == 'test':
        information = {
            "Name": decoded[-3],
            "Surname": decoded[-5],
            "DateOfBirth": decoded[-1],
            "Producer": expirations[decoded[2]][0],
            "DateOfTest": decoded[1],
            "Place": decoded[5],
            "Code": decoded[6],
            "State": decoded[4],
            "IssuingBody": decoded[7]
        }
    else:
        information = {
            "Name": decoded[-3],
            "Surname": decoded[-5],
            "DateOfBirth": decoded[-1],
            "VaxCode": decoded[3],
            "Vax": decoded[7],
            "Producer": expirations[decoded[2]][0],
            "NumberDoses": decoded[1],
            "DateOfVaxination": decoded[4],
            "Code": decoded[6],
            "State": decoded[5],
            "IssuingBody": decoded[8]
        }

    return information
