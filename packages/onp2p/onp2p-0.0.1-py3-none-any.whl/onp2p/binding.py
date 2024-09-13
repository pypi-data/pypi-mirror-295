from cffi import FFI

ffibuilder = FFI()

# Dichiarazione delle funzioni C
ffibuilder.cdef("""
    int add(int a, int b);
    int multiply(int a, int b);
""")

# Aggiungiamo il file C da compilare
ffibuilder.set_source(
    "_onp2p",               # Nome del modulo Python generato
    """
    #include "math_operations.c"
    """,
    sources=["math_operations.c"]  # File sorgente C
)

# Compiliamo il modulo
if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
