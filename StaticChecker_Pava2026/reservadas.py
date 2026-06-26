
PALAVRAS_RESERVADAS = {
    "BOOLEAN":          "A01",
    "BREAK":            "A02",
    "CHARACTER":        "A03",
    "DECLARATIONS":     "A04",
    "ELSE":             "A05",
    "ENDDECLARACIONS":  "A06",
    "ENDFUNCTION":      "A07",
    "ENDFUNCTIONS":     "A08",
    "ENDIF":            "A09",
    "ENDPROGRAM":       "A10",
    "ENDWHILE":         "A11",
    "FALSE":            "A12",
    "FUNCTIONS":        "A13",
    "FUNCTYPE":         "A14",
    "IF":               "A15",
    "INTEGER":          "A16",
    "PARAMTYPE":        "A17",
    "PRINT":            "A18",
    "PROGRAM":          "A19",
    "REAL":             "A20",
    "RETURN":           "A21",
    "STRING":           "A22",
    "TRUE":             "A23",
    "VARTYPE":          "A24",
    "VOID":             "A25",
    "WHILE":            "A26",
}


SIMBOLOS_RESERVADOS = [
    ("<=",  "B20"),
    (">=",  "B22"),
    ("==",  "B17"),
    ("!=",  "B18"),
    (":=",  "B04"),
    (";",   "B01"),
    (",",   "B02"),
    (":",   "B03"),
    ("?",   "B05"),
    ("(",   "B06"),
    (")",   "B07"),
    ("[",   "B08"),
    ("]",   "B09"),
    ("{",   "B10"),
    ("}",   "B11"),
    ("+",   "B12"),
    ("-",   "B13"),
    ("*",   "B14"),
    ("/",   "B15"),
    ("%",   "B16"),
    ("#",   "B18"),
    ("<",   "B19"),
    (">",   "B21"),
]

def get_codigo_palavra(lexeme_maiusculo: str):
    return PALAVRAS_RESERVADAS.get(lexeme_maiusculo)

def get_codigo_simbolo(texto: str, pos: int):
    
    for simbolo, codigo in SIMBOLOS_RESERVADOS:
        tamanho = len(simbolo)
        trecho = texto[pos:pos + tamanho]
        if trecho == simbolo:
            return simbolo, codigo
    return None, None
