# Ledger V31.3 · Calendar hotfix

Corrección:
- En el detalle del calendario, los movimientos 2º, 3º, 4º... podían mostrarse como 0,00 € aunque su importe real fuese correcto.
- La causa era `dayTx.map(transactionRow)`, que pasaba el índice del array como segundo parámetro de `transactionRow`.
- Se cambia a `dayTx.map(t => transactionRow(t))`.

No se modifica:
- datos
- layout
- branding Ledger by ARX
- categorías
- navegación
- clave local `flowfi.public.v27`
