import os
import flet as ft
import pandas as pd

# Archivo de Excel de Suministros y Accesorios Carabobo
EXCEL_FILE = "S-A-C-202200923 .xlsx"


def cargar_datos():
  if not os.path.exists(EXCEL_FILE):
    return None
  try:
    xls = pd.ExcelFile(EXCEL_FILE)
    df_inv = pd.read_excel(xls, sheet_name="INV").dropna(subset=["PRODUCTO"])
    return df_inv
  except Exception as e:
    print(f"Error al leer el Excel: {e}")
    return None


def main(page: ft.Page):
  page.title = "S.A.C. Móvil - Suministros y Accesorios Carabobo"
  page.theme_mode = ft.ThemeMode.LIGHT
  page.padding = 12
  page.window_width = 400
  page.window_height = 750

  df_inv = cargar_datos()

  if df_inv is None:
    page.add(
        ft.Text(
            "⚠️ No se encontró el archivo Excel 'S-A-C-202200923 .xlsx' en la"
            " misma carpeta.",
            color=ft.colors.RED_700,
            weight=ft.FontWeight.BOLD,
        )
    )
    return

  # Encabezado Comercial
  header = ft.Container(
      content=ft.Column(
          [
              ft.Text(
                  "⚙️ S.A.C. CARABOBO",
                  size=17,
                  weight=ft.FontWeight.BOLD,
                  color=ft.colors.BLUE_900,
              ),
              ft.Text(
                  "Av. Andrés Bello c/c López, Guacara",
                  size=11,
                  color=ft.colors.GREY_700,
              ),
          ],
          spacing=2,
      ),
      padding=10,
      bgcolor=ft.colors.BLUE_50,
      border_radius=8,
  )

  # Buscador de productos
  search_input = ft.TextField(
      label="Buscar producto, código o referencia...",
      prefix_icon=ft.icons.SEARCH,
      border_radius=8,
      text_size=13,
  )

  inv_list = ft.ListView(expand=1, spacing=8, padding=2)

  def actualizar_lista(query=""):
    inv_list.controls.clear()
    filtered = df_inv
    if query:
      q = query.lower()
      filtered = df_inv[
          df_inv["PRODUCTO"].astype(str).str.lower().str.contains(q, na=False)
          | df_inv["CÓDIGO"].astype(str).str.lower().str.contains(q, na=False)
          | df_inv["COD. REF."].astype(str).str.lower().str.contains(q, na=False)
      ]

    for _, row in filtered.iterrows():
      costo = row["COSTO EN DIVISAS"]
      costo_str = f"${costo:,.2f}" if pd.notna(costo) else "A consultar"
      inv_list.controls.add(
          ft.Card(
              content=ft.Container(
                  content=ft.Column(
                      [
                          ft.Row(
                              [
                                  ft.Text(
                                      f"[{row['CÓDIGO']}]",
                                      weight=ft.FontWeight.BOLD,
                                      color=ft.colors.BLUE_700,
                                      size=12,
                                  ),
                                  ft.Text(
                                      f"Ref: {row['COD. REF.']}",
                                      size=11,
                                      color=ft.colors.GREY_600,
                                  ),
                              ],
                              alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                          ),
                          ft.Text(
                              str(row["PRODUCTO"]),
                              size=12,
                              weight=ft.FontWeight.W_500,
                          ),
                          ft.Row(
                              [
                                  ft.Text(
                                      "Costo Divisas:",
                                      size=11,
                                      color=ft.colors.GREY_700,
                                  ),
                                  ft.Text(
                                      costo_str,
                                      size=12,
                                      weight=ft.FontWeight.BOLD,
                                      color=ft.colors.GREEN_700,
                                  ),
                              ],
                              alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                          ),
                      ],
                      spacing=3,
                  ),
                  padding=10,
              )
          )
      )
    page.update()

  search_input.on_change = lambda e: actualizar_lista(search_input.value)
  actualizar_lista()

  tab_inv = ft.Column([search_input, ft.Divider(height=4), inv_list], expand=True)

  # Pestaña de Cotización / Nota Rápida
  cliente_input = ft.TextField(
      label="Nombre del Cliente / Empresa", text_size=13, border_radius=8
  )
  tasa_input = ft.TextField(
      label="Tasa BCV (Bs / $)",
      value="36.5",
      text_size=13,
      keyboard_type=ft.KeyboardType.NUMBER,
      border_radius=8,
  )

  tab_cot = ft.Column(
      [
          cliente_input,
          tasa_input,
          ft.Divider(height=10),
          ft.Text(
              "📄 Generación de Nota de Entrega",
              size=14,
              weight=ft.FontWeight.BOLD,
          ),
          ft.Text(
              "Selecciona artículos del inventario para calcular totales automáticos en divisas y bolívares.",
              size=11,
              color=ft.colors.GREY_600,
          ),
      ],
      expand=True,
      spacing=10,
  )

  content_area = ft.Container(content=tab_inv, expand=True)

  def cambiar_pestana(e):
    if e.control.selected_index == 0:
      content_area.content = tab_inv
    else:
      content_area.content = tab_cot
    page.update()

  navbar = ft.NavigationBar(
      destinations=[
          ft.NavigationDestination(
              icon=ft.icons.INVENTORY_2_OUTLINED,
              selected_icon=ft.icons.INVENTORY_2,
              label="Inventario",
          ),
          ft.NavigationDestination(
              icon=ft.icons.RECEIPT_LONG_OUTLINED,
              selected_icon=ft.icons.RECEIPT_LONG,
              label="Cotizar",
          ),
      ],
      on_change=cambiar_pestana,
  )

  page.add(header, content_area, navbar)


if __name__ == "__main__":
  ft.app(target=main)
  