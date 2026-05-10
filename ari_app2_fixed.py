import json
import os
from io import BytesIO, StringIO

import pandas as pd
import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# =========================================================
# ARI — AI DATA ANALYST APP
# Clean Streamlit MVP with ARI branding
# =========================================================

st.set_page_config(
    page_title="ari. — AI Data Analyst",
    page_icon="ari_robot.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #ffffff;
        color: #111111;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    h1 {
        font-size: 3.1rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.055em !important;
        margin-bottom: 0.2rem !important;
    }

    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.035em !important;
        color: #111111 !important;
    }

    .ari-blue {
        color: #0A84FF;
    }

    .ari-hero {
        border: 1px solid #eeeeee;
        border-radius: 28px;
        padding: 0.8rem 1.6rem;
        margin-bottom: 1.4rem;
        background: linear-gradient(180deg, #ffffff 0%, #fbfbfb 100%);
    }

    .ari-logo-title {
        font-size: 3.4rem;
        font-weight: 600;
        letter-spacing: -0.065em;
        line-height: 1;
        color: #111111;
    }

    .ari-logo-dot {
        color: #0A84FF;
    }

    .ari-subtitle {
        font-size: 1.08rem;
        color: #555555;
        line-height: 1.55;
        max-width: 720px;
        margin-top: 0.75rem;
    }

    .ari-card {
        border: 1px solid #eeeeee;
        border-radius: 22px;
        padding: 1.2rem 1.25rem;
        background: #ffffff;
        box-shadow: 0 8px 30px rgba(0,0,0,0.035);
        height: 100%;
    }

    .ari-card-soft {
        border: 1px solid #eeeeee;
        border-radius: 22px;
        padding: 1.2rem 1.25rem;
        background: #fafafa;
        height: 100%;
    }

    .ari-small-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #777777;
        margin-bottom: 0.35rem;
    }

    .ari-big-number {
        font-size: 2rem;
        font-weight: 650;
        letter-spacing: -0.045em;
        color: #111111;
    }

    .ari-muted {
        color: #666666;
        font-size: 0.94rem;
        line-height: 1.45;
    }

    .ari-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        border: 1px solid #eeeeee;
        border-radius: 999px;
        padding: 0.38rem 0.75rem;
        background: #ffffff;
        color: #333333;
        font-size: 0.86rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    [data-testid="stSidebar"] {
        background: #fbfbfb;
        border-right: 1px solid #eeeeee;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        letter-spacing: -0.035em !important;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #eeeeee;
        border-radius: 22px;
        padding: 1rem 1.1rem;
        background: #ffffff;
        box-shadow: 0 8px 26px rgba(0,0,0,0.025);
    }

    div[data-testid="stMetric"] label {
        color: #777777 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }

    div[data-testid="stMetricValue"] {
        color: #111111 !important;
        font-size: 1.75rem !important;
        font-weight: 650 !important;
        letter-spacing: -0.045em;
    }

    .stButton > button {
        background: #111111;
        color: #ffffff;
        border: 1px solid #111111;
        border-radius: 999px;
        padding: 0.55rem 1.1rem;
        font-weight: 600;
        transition: 0.15s ease;
    }

    .stButton > button:hover {
        background: #0A84FF;
        border-color: #0A84FF;
        color: #ffffff;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid #eeeeee;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 0.55rem 1rem;
        color: #444444;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: #111111 !important;
        color: #ffffff !important;
    }

    [data-testid="stChatMessage"] {
        border-radius: 22px;
        border: 1px solid #eeeeee;
        background: #ffffff;
        padding: 0.8rem 1rem;
        box-shadow: 0 8px 26px rgba(0,0,0,0.025);
    }

    .stChatInputContainer {
        border-top: 1px solid #eeeeee;
    }

    .ari-separator {
        height: 1px;
        background: #eeeeee;
        margin: 1rem 0 1.25rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LANGUAGE TEXT
# =========================================================

TEXT = {
    "en": {
        "app_name": "ari.",
        "hero_title": "ari<span class='ari-logo-dot'>.</span>",
        "hero_subtitle": "Your AI Data Analyst for small brands. Upload your sales data, understand what is happening, and ask ARI what to do next.",
        "sidebar_brand": "ari.",
        "sidebar_role": "AI Data Analyst",
        "upload_step": "1. Upload your data",
        "context_step": "2. Business context",
        "language_step": "3. Language",
        "tip_title": "Tip",
        "tip_text": "The better the context, the more useful ARI's answers become.",
        "upload_label": "CSV or Excel file",
        "business_context": "Choose your business type",
        "file_loaded": "Loaded file",
        "selected_context": "Business context",
        "column_mapping": "Column mapping",
        "apply_columns": "Apply selected columns",
        "manual_revenue": "Revenue column",
        "manual_product": "Product column",
        "manual_date": "Date column",
        "manual_category": "Category column",
        "manual_region": "Region / city column",
        "manual_customer": "Customer column",
        "manual_order": "Order column",
        "warnings": "Warnings",
        "analysis_complete": "Analysis complete",
        "new_analysis": "New analysis loaded. Chat history cleared.",
        "kpis": "Key Metrics",
        "total_revenue": "Total Revenue",
        "total_orders": "Total Orders",
        "total_rows": "Total Rows",
        "average_revenue": "Average Revenue",
        "overview_tab": "Overview",
        "products_tab": "Products",
        "customers_tab": "Customers",
        "regions_tab": "Regions",
        "chat_tab": "Chat with ARI",
        "summary": "ARI's Summary",
        "generate_summary": "Generate summary",
        "summary_loading": "ARI is preparing your summary...",
        "preview": "Data Preview",
        "quick_insights": "Key Insights",
        "quick_actions": "Suggested Actions",
        "trend": "Revenue Trend",
        "top_products": "Top Products",
        "bottom_products": "Bottom Products",
        "category": "Revenue by Category",
        "customer": "Revenue by Customer Group",
        "region": "Revenue by Region",
        "map": "Order Map",
        "generate_map": "Generate map",
        "map_loading": "ARI is building your map...",
        "map_note": "The map is generated only when requested, so the app stays faster.",
        "no_map": "No geographic map available. A city/region column is required.",
        "no_chart": "No data available for this chart.",
        "chat_title": "Talk to ARI",
        "chat_empty": "Try asking: Which products should I focus on? Why is revenue changing? What should I do next?",
        "chat_placeholder": "Ask ARI anything about your data...",
        "chat_loading": "ARI is thinking...",
        "missing_key": "OPENAI_API_KEY is not configured on the server.",
        "upload_info": "Upload a CSV or Excel file to start.",
        "ari_intro": "Hi, I'm ARI. I can read your data, explain what matters, and help you decide what to do next.",
    },
    "it": {
        "app_name": "ari.",
        "hero_title": "ari<span class='ari-logo-dot'>.</span>",
        "hero_subtitle": "La tua AI Data Analyst per piccoli brand. Carica i dati di vendita, capisci cosa sta succedendo e chiedi ad ARI cosa fare dopo.",
        "sidebar_brand": "ari.",
        "sidebar_role": "AI Data Analyst",
        "upload_step": "1. Carica i tuoi dati",
        "context_step": "2. Contesto del business",
        "language_step": "3. Lingua",
        "tip_title": "Suggerimento",
        "tip_text": "Più il contesto è preciso, più le risposte di ARI saranno utili.",
        "upload_label": "File CSV o Excel",
        "business_context": "Scegli il tipo di business",
        "file_loaded": "File caricato",
        "selected_context": "Contesto del business",
        "column_mapping": "Mappatura colonne",
        "apply_columns": "Applica colonne selezionate",
        "manual_revenue": "Colonna revenue",
        "manual_product": "Colonna prodotto",
        "manual_date": "Colonna data",
        "manual_category": "Colonna categoria",
        "manual_region": "Colonna regione / città",
        "manual_customer": "Colonna cliente",
        "manual_order": "Colonna ordine",
        "warnings": "Avvisi",
        "analysis_complete": "Analisi completata",
        "new_analysis": "Nuova analisi caricata. Chat azzerata.",
        "kpis": "Metriche chiave",
        "total_revenue": "Fatturato totale",
        "total_orders": "Ordini totali",
        "total_rows": "Righe totali",
        "average_revenue": "Revenue media",
        "overview_tab": "Panoramica",
        "products_tab": "Prodotti",
        "customers_tab": "Clienti",
        "regions_tab": "Regioni",
        "chat_tab": "Chat con ARI",
        "summary": "Sintesi di ARI",
        "generate_summary": "Genera sintesi",
        "summary_loading": "ARI sta preparando la sintesi...",
        "preview": "Anteprima dati",
        "quick_insights": "Insight chiave",
        "quick_actions": "Azioni suggerite",
        "trend": "Andamento del fatturato",
        "top_products": "Prodotti migliori",
        "bottom_products": "Prodotti peggiori",
        "category": "Fatturato per categoria",
        "customer": "Fatturato per gruppo clienti",
        "region": "Fatturato per regione",
        "map": "Mappa ordini",
        "generate_map": "Genera mappa",
        "map_loading": "ARI sta costruendo la mappa...",
        "map_note": "La mappa viene generata solo quando richiesta, così l'app resta più veloce.",
        "no_map": "Nessuna mappa disponibile. Serve una colonna città/regione.",
        "no_chart": "Nessun dato disponibile per questo grafico.",
        "chat_title": "Parla con ARI",
        "chat_empty": "Prova a chiedere: Su quali prodotti dovrei puntare? Perché il fatturato cambia? Cosa dovrei fare adesso?",
        "chat_placeholder": "Fai una domanda ad ARI sui tuoi dati...",
        "chat_loading": "ARI sta pensando...",
        "missing_key": "OPENAI_API_KEY non è configurata sul server.",
        "upload_info": "Carica un file CSV o Excel per iniziare.",
        "ari_intro": "Ciao, sono ARI. Posso leggere i tuoi dati, spiegarti cosa conta davvero e aiutarti a decidere cosa fare dopo.",
    },
}

CONTEXT_OPTIONS = {
    "en": {
        "Handmade brand": "Small handmade brand selling products online.",
        "Fashion brand": "Small fashion brand selling online.",
        "Accessories brand": "Small accessories brand selling online.",
        "Beauty brand": "Small beauty brand selling online.",
        "General small business": "Small product-based business selling online.",
    },
    "it": {
        "Brand artigianale": "Piccolo brand artigianale che vende prodotti online.",
        "Brand moda": "Piccolo brand di moda che vende online.",
        "Brand accessori": "Piccolo brand di accessori che vende online.",
        "Brand beauty": "Piccolo brand beauty che vende online.",
        "Piccolo business generico": "Piccolo business che vende prodotti online.",
    },
}


# =========================================================
# SESSION STATE
# =========================================================

for key, default in {
    "chat_history": [],
    "current_file": None,
    "ai_summary": None,
    "map_df": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# =========================================================
# DATA FUNCTIONS
# =========================================================

@st.cache_data(show_spinner=False)
def read_uploaded_table(filename: str, content: bytes) -> pd.DataFrame:
    lower = filename.lower()

    if lower.endswith(".csv"):
        try:
            return pd.read_csv(StringIO(content.decode("utf-8")))
        except UnicodeDecodeError:
            return pd.read_csv(StringIO(content.decode("latin-1")))

    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return pd.read_excel(BytesIO(content))

    raise ValueError("Only CSV and Excel files are supported.")


def find_columns(df: pd.DataFrame) -> dict:
    cols = list(df.columns)

    def match(words):
        return [c for c in cols if any(w in c.lower() for w in words)]

    return {
        "revenue": match(["revenue", "sales", "gross_sales", "amount", "total", "price", "fatturato", "ricavi", "vendite"]),
        "product": match(["product", "item", "sku", "item_name", "product_name", "name", "prodotto", "articolo"]),
        "date": match(["date", "created_at", "created", "time", "day", "data", "giorno"]),
        "category": match(["category", "segment", "type", "categoria", "tipo"]),
        "region": match(["region", "city", "city_zone", "area", "location", "città", "citta", "regione", "provincia"]),
        "customer": match(["customer_type", "buyer_group", "customer", "client", "user_type", "cliente", "segmento"]),
        "order": match(["order_id", "order", "invoice", "invoice_code", "ordine", "fattura"]),
    }


def safe_records(obj):
    if obj is None:
        return None
    if isinstance(obj, pd.DataFrame):
        return obj.fillna("").to_dict(orient="records")
    return obj


def build_warnings(result: dict, lang: str) -> list[str]:
    detected = result["detected_columns"]
    warnings = []

    if not detected["revenue"]:
        warnings.append("No revenue column detected." if lang == "en" else "Nessuna colonna revenue rilevata.")
    if not detected["date"]:
        warnings.append(
            "No date column detected, so trend analysis may be limited."
            if lang == "en"
            else "Nessuna colonna data rilevata, quindi il trend potrebbe essere limitato."
        )
    if not detected["product"]:
        warnings.append(
            "No product column detected, so product analysis may be limited."
            if lang == "en"
            else "Nessuna colonna prodotto rilevata, quindi l'analisi prodotti potrebbe essere limitata."
        )

    return warnings


def analyze(df: pd.DataFrame, lang: str, selected_columns: dict | None = None) -> dict:
    working = df.copy()
    found = find_columns(working)

    def choose(key: str):
        if selected_columns and selected_columns.get(key):
            return selected_columns[key]
        return found[key][0] if found[key] else None

    revenue_col = choose("revenue")
    product_col = choose("product")
    date_col = choose("date")
    category_col = choose("category")
    region_col = choose("region")
    customer_col = choose("customer")
    order_col = choose("order")

    result = {
        "detected_columns": {
            "revenue": revenue_col,
            "product": product_col,
            "date": date_col,
            "category": category_col,
            "region": region_col,
            "customer": customer_col,
            "order": order_col,
        },
        "kpis": {},
        "top_products": None,
        "bottom_products": None,
        "trend": None,
        "category_breakdown": None,
        "region_breakdown": None,
        "customer_breakdown": None,
        "rule_based_insights": [],
        "rule_based_recommendations": [],
    }

    if revenue_col:
        working["_rev"] = pd.to_numeric(working[revenue_col], errors="coerce")
        result["kpis"]["total_revenue"] = float(working["_rev"].sum())
        result["kpis"]["average_revenue"] = float(working["_rev"].mean()) if working["_rev"].notna().any() else 0.0

    if order_col:
        result["kpis"]["total_orders"] = int(working[order_col].nunique())
    else:
        result["kpis"]["total_rows"] = int(len(working))

    if product_col and revenue_col:
        grouped = working.groupby(product_col, dropna=False)["_rev"].sum().sort_values(ascending=False)
        result["top_products"] = grouped.head(5).reset_index()
        result["bottom_products"] = grouped.tail(5).reset_index()

        if len(grouped) > 0 and result["kpis"].get("total_revenue", 0) > 0:
            top_name = str(grouped.index[0])
            top_value = float(grouped.iloc[0])
            contribution = top_value / result["kpis"]["total_revenue"] * 100

            if lang == "it":
                result["rule_based_insights"].append(f"Il prodotto principale '{top_name}' genera il {contribution:.1f}% del fatturato totale.")
                result["rule_based_recommendations"].append(f"Aumenta la visibilità e il focus marketing su '{top_name}'.")
            else:
                result["rule_based_insights"].append(f"Top product '{top_name}' generates {contribution:.1f}% of total revenue.")
                result["rule_based_recommendations"].append(f"Increase visibility and marketing focus on '{top_name}'.")

    if date_col and revenue_col:
        temp = working.copy()
        temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
        temp = temp.dropna(subset=[date_col])

        if not temp.empty:
            trend = temp.groupby(temp[date_col].dt.to_period("M"))["_rev"].sum().reset_index()
            trend[date_col] = trend[date_col].astype(str)
            result["trend"] = trend

            if len(trend) >= 2:
                prev_val = float(trend.iloc[-2]["_rev"])
                curr_val = float(trend.iloc[-1]["_rev"])
                if prev_val != 0:
                    pct = (curr_val - prev_val) / prev_val * 100
                    if lang == "it":
                        direction = "aumentato" if pct >= 0 else "diminuito"
                        result["rule_based_insights"].append(f"Il fatturato è {direction} del {abs(pct):.1f}% nell'ultimo mese rispetto al precedente.")
                    else:
                        direction = "increased" if pct >= 0 else "decreased"
                        result["rule_based_insights"].append(f"Revenue {direction} by {abs(pct):.1f}% in the latest month versus the previous month.")

    if category_col and revenue_col:
        result["category_breakdown"] = working.groupby(category_col, dropna=False)["_rev"].sum().sort_values(ascending=False).reset_index()

    if region_col and revenue_col:
        result["region_breakdown"] = working.groupby(region_col, dropna=False)["_rev"].sum().sort_values(ascending=False).reset_index()

    if customer_col and revenue_col:
        result["customer_breakdown"] = working.groupby(customer_col, dropna=False)["_rev"].sum().sort_values(ascending=False).reset_index()

    if revenue_col and "total_revenue" in result["kpis"]:
        total = result["kpis"]["total_revenue"]
        if lang == "it":
            result["rule_based_insights"].append(f"Nel dataset caricato è stato rilevato un fatturato totale di {total:.2f}.")
            result["rule_based_recommendations"].append("Analizza i prodotti più deboli e testa bundle, modifiche di prezzo o promozioni.")
        else:
            result["rule_based_insights"].append(f"Detected total revenue of {total:.2f} in the uploaded dataset.")
            result["rule_based_recommendations"].append("Review weak products and test bundles, pricing changes, or promotions.")

    if category_col and result["category_breakdown"] is not None and len(result["category_breakdown"]) > 0:
        top_cat = result["category_breakdown"].iloc[0]
        total = result["kpis"].get("total_revenue", 0)
        if total:
            pct = float(top_cat["_rev"]) / total * 100
            if lang == "it":
                result["rule_based_insights"].append(f"La categoria principale '{top_cat[category_col]}' contribuisce per il {pct:.1f}% al fatturato totale.")
            else:
                result["rule_based_insights"].append(f"Top category '{top_cat[category_col]}' contributes {pct:.1f}% of total revenue.")

    if customer_col and result["customer_breakdown"] is not None and len(result["customer_breakdown"]) > 0:
        top_group = result["customer_breakdown"].iloc[0]
        if lang == "it":
            result["rule_based_recommendations"].append(f"Crea azioni mirate per il gruppo clienti '{top_group[customer_col]}', che attualmente genera il fatturato più alto.")
        else:
            result["rule_based_recommendations"].append(f"Create targeted actions for customer group '{top_group[customer_col]}', which currently drives the highest revenue.")

    return result


# =========================================================
# MAP FUNCTIONS
# =========================================================

@st.cache_data(show_spinner=False)
def geocode_places(places: list[str]) -> dict:
    from geopy.extra.rate_limiter import RateLimiter
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="ari-ai-data-analyst")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    coords = {}
    for raw in places:
        place = str(raw).strip()
        if not place:
            continue
        try:
            location = geocode(place)
            coords[raw] = (location.latitude, location.longitude) if location else (None, None)
        except Exception:
            coords[raw] = (None, None)
    return coords


def build_order_map(df: pd.DataFrame, region_col: str, order_col: str | None = None, revenue_col: str | None = None):
    map_df = df.copy()
    places = [p for p in map_df[region_col].dropna().astype(str).unique().tolist() if p.strip()]
    if not places:
        return None

    coords = geocode_places(places)
    map_df["lat"] = map_df[region_col].map(lambda x: coords.get(str(x), (None, None))[0])
    map_df["lon"] = map_df[region_col].map(lambda x: coords.get(str(x), (None, None))[1])
    map_df = map_df.dropna(subset=["lat", "lon"])

    if map_df.empty:
        return None

    if revenue_col and "_rev" in map_df.columns:
        return map_df.groupby(region_col, dropna=False).agg(
            orders=(order_col, "nunique") if order_col else (region_col, "size"),
            revenue=("_rev", "sum"),
            lat=("lat", "first"),
            lon=("lon", "first"),
        ).reset_index()

    result = map_df.groupby(region_col, dropna=False).agg(
        orders=(order_col, "nunique") if order_col else (region_col, "size"),
        lat=("lat", "first"),
        lon=("lon", "first"),
    ).reset_index()
    result["revenue"] = None
    return result


# =========================================================
# AI FUNCTIONS
# =========================================================

def get_openai_client():
    if OpenAI is None:
        return None
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def build_system_prompt(lang: str) -> str:
    if lang == "it":
        return (
            "Sei ARI, una AI Data Analyst per piccoli business. "
            "Parla in modo naturale, umano, chiaro e conversazionale. "
            "Devi sembrare una vera analista, non un robot freddo. "
            "Spiega i dati in modo semplice e collega sempre i numeri alle decisioni concrete. "
            "Se i dati non bastano, dillo chiaramente. Rispondi sempre in italiano."
        )
    return (
        "You are ARI, an AI Data Analyst for small businesses. "
        "Speak in a natural, human, clear, and conversational tone. "
        "You should feel like a real analyst, not a cold robot. "
        "Explain data simply and always connect numbers to concrete business decisions. "
        "If the data is not enough, say so clearly. Always respond in English."
    )


def build_analysis_context(result: dict) -> dict:
    return {
        "detected_columns": result.get("detected_columns", {}),
        "kpis": result.get("kpis", {}),
        "top_products": safe_records(result.get("top_products")),
        "bottom_products": safe_records(result.get("bottom_products")),
        "trend": safe_records(result.get("trend")),
        "category_breakdown": safe_records(result.get("category_breakdown")),
        "region_breakdown": safe_records(result.get("region_breakdown")),
        "customer_breakdown": safe_records(result.get("customer_breakdown")),
        "rule_based_insights": result.get("rule_based_insights", []),
        "rule_based_recommendations": result.get("rule_based_recommendations", []),
    }


def generate_ai_summary(result: dict, brand_context: str, lang: str) -> str:
    client = get_openai_client()
    if client is None:
        return TEXT[lang]["missing_key"]

    payload = build_analysis_context(result)

    if lang == "it":
        prompt = f"""
Contesto business:
{brand_context}

Dati analizzati:
{json.dumps(payload, indent=2, ensure_ascii=False)}

Scrivi una sintesi come farebbe una vera data analyst.

Struttura:
1. Breve overview iniziale
2. 4 insight chiave
3. 4 azioni consigliate

Regole:
- Non inventare dati
- Sii chiara, umana e concreta
- Parla come se stessi aiutando direttamente il titolare del business
"""
    else:
        prompt = f"""
Business context:
{brand_context}

Analyzed data:
{json.dumps(payload, indent=2, ensure_ascii=False)}

Write a summary like a real data analyst would.

Structure:
1. Short opening overview
2. 4 key insights
3. 4 recommended actions

Rules:
- Do not invent data
- Be clear, human, and practical
- Speak as if you are directly helping the business owner
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_prompt(lang)},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def answer_chat_question(question: str, analysis_context: dict, chat_history: list, brand_context: str, lang: str) -> str:
    client = get_openai_client()
    if client is None:
        return TEXT[lang]["missing_key"]

    compact_context = {
        "kpis": analysis_context.get("kpis", {}),
        "top_products": (analysis_context.get("top_products") or [])[:5],
        "bottom_products": (analysis_context.get("bottom_products") or [])[:5],
        "trend": (analysis_context.get("trend") or [])[-6:],
        "category_breakdown": (analysis_context.get("category_breakdown") or [])[:5],
        "region_breakdown": (analysis_context.get("region_breakdown") or [])[:5],
        "customer_breakdown": (analysis_context.get("customer_breakdown") or [])[:5],
        "rule_based_insights": analysis_context.get("rule_based_insights", []),
        "rule_based_recommendations": analysis_context.get("rule_based_recommendations", []),
    }

    if lang == "it":
        prompt = f"""
Contesto business:
{brand_context}

Contesto analisi:
{json.dumps(compact_context, indent=2, ensure_ascii=False)}

Storico conversazione:
{json.dumps(chat_history[-6:], indent=2, ensure_ascii=False)}

Domanda utente:
{question}

Rispondi come ARI, una data analyst umana e utile.
Usa solo i dati forniti. Se i dati non bastano, dillo chiaramente.
Concludi con un consiglio pratico quando possibile.
"""
    else:
        prompt = f"""
Business context:
{brand_context}

Analysis context:
{json.dumps(compact_context, indent=2, ensure_ascii=False)}

Conversation history:
{json.dumps(chat_history[-6:], indent=2, ensure_ascii=False)}

User question:
{question}

Answer as ARI, a human and helpful data analyst.
Use only the provided data. If the data is not enough, say so clearly.
End with a practical recommendation when possible.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_prompt(lang)},
            {"role": "user", "content": prompt},
        ],
        temperature=0.35,
    )
    return response.choices[0].message.content


# =========================================================
# UI HELPERS
# =========================================================

def show_logo(width: int = 220):
    """Display ARI logo from the current project folder.

    Keep file paths relative so the app works on any computer and after deploy.
    Preferred file: ari_robot.svg. Fallback: ari_robot.png.
    """
    if os.path.exists("ari_robot.svg"):
        st.image("ari_robot.svg", width=width)
    elif os.path.exists("ari_robot.png"):
        st.image("ari_robot.png", width=width)
    else:
        st.markdown(
            """
            <div style="
                font-size:2.2rem;
                font-weight:600;
                letter-spacing:-0.06em;
                text-align:center;
            ">
                ari<span style='color:#0A84FF'>.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

def plot_bar(df: pd.DataFrame, label_col: str, value_col: str = "_rev"):
    import plotly.express as px

    fig = px.bar(df, x=label_col, y=value_col)
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111111", family="Inter"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=360,
    )
    fig.update_traces(marker_color="#111111")
    return fig


def plot_line(df: pd.DataFrame, x_col: str, y_col: str = "_rev"):
    import plotly.express as px

    fig = px.line(df, x=x_col, y=y_col, markers=True)
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111111", family="Inter"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=380,
    )
    fig.update_traces(line_color="#0A84FF", marker=dict(color="#0A84FF", size=8))
    return fig


# =========================================================
# SIDEBAR
# =========================================================

language_label = st.sidebar.selectbox("Language", ["English", "Italiano"], index=1)
lang = "it" if language_label == "Italiano" else "en"
T = TEXT[lang]

with st.sidebar:
    show_logo(width=180)
    st.markdown(f"### {T['sidebar_brand']}")
    st.caption(T["sidebar_role"])

    st.markdown("<div class='ari-separator'></div>", unsafe_allow_html=True)
    st.markdown(f"**{T['upload_step']}**")
    uploaded_file = st.file_uploader(T["upload_label"], type=["csv", "xlsx", "xls"])

    st.markdown("<div class='ari-separator'></div>", unsafe_allow_html=True)
    st.markdown(f"**{T['context_step']}**")
    selected_context_label = st.selectbox(T["business_context"], list(CONTEXT_OPTIONS[lang].keys()))
    brand_context = CONTEXT_OPTIONS[lang][selected_context_label]
    st.caption(brand_context)

    st.markdown("<div class='ari-separator'></div>", unsafe_allow_html=True)
    st.markdown(f"**{T['language_step']}**")
    st.write(language_label)

    st.markdown("<div class='ari-separator'></div>", unsafe_allow_html=True)
    st.markdown(f"**{T['tip_title']}**")
    st.info(T["tip_text"])


# =========================================================
# HERO
# =========================================================

hero_left, hero_right = st.columns([0.55, 4.45])

with hero_left:
    st.image("logo.svg", width=42)

with hero_right:
    st.markdown(
        """
        <div class="ari-hero">
        """,
        unsafe_allow_html=True,
    )

    show_logo(width=300)

    st.markdown(
        f"""
            <div class="ari-subtitle">{T['hero_subtitle']}</div>
            <div style="margin-top:1rem;">
                <span class="ari-pill">AI Analyst</span>
                <span class="ari-pill">CSV / Excel</span>
                <span class="ari-pill">Insights</span>
                <span class="ari-pill">Chat</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if uploaded_file is None:
    st.info(T["upload_info"])
    st.stop()


# =========================================================
# LOAD + COLUMN MAPPING
# =========================================================

file_id = f"{uploaded_file.name}_{uploaded_file.size}"
if st.session_state.current_file != file_id:
    st.session_state.current_file = file_id
    st.session_state.chat_history = []
    st.session_state.ai_summary = None
    st.session_state.map_df = None
    st.success(T["new_analysis"])

df = read_uploaded_table(uploaded_file.name, uploaded_file.getvalue())
found = find_columns(df)

st.markdown(f"**{T['file_loaded']}:** {uploaded_file.name}")
st.markdown(f"**{T['selected_context']}:** {selected_context_label}")

with st.expander(T["column_mapping"], expanded=False):
    with st.form("column_selection_form"):
        columns_options = [""] + list(df.columns)

        def default_index(key):
            if found[key] and found[key][0] in df.columns:
                return columns_options.index(found[key][0])
            return 0

        manual_columns = {
            "revenue": st.selectbox(T["manual_revenue"], columns_options, index=default_index("revenue")),
            "product": st.selectbox(T["manual_product"], columns_options, index=default_index("product")),
            "date": st.selectbox(T["manual_date"], columns_options, index=default_index("date")),
            "category": st.selectbox(T["manual_category"], columns_options, index=default_index("category")),
            "region": st.selectbox(T["manual_region"], columns_options, index=default_index("region")),
            "customer": st.selectbox(T["manual_customer"], columns_options, index=default_index("customer")),
            "order": st.selectbox(T["manual_order"], columns_options, index=default_index("order")),
        }
        st.form_submit_button(T["apply_columns"])

manual_columns = {k: v if v else None for k, v in manual_columns.items()}

result = analyze(df, lang, manual_columns)
warnings = build_warnings(result, lang)
analysis_context = build_analysis_context(result)

st.success(T["analysis_complete"])
if warnings:
    st.subheader(T["warnings"])
    for warning in warnings:
        st.warning(warning)


# =========================================================
# KPI
# =========================================================

st.subheader(T["kpis"])
k1, k2, k3 = st.columns(3)
with k1:
    st.metric(T["total_revenue"], f"{result['kpis'].get('total_revenue', 0):,.2f}")
with k2:
    if "total_orders" in result["kpis"]:
        st.metric(T["total_orders"], result["kpis"]["total_orders"])
    else:
        st.metric(T["total_rows"], result["kpis"].get("total_rows", 0))
with k3:
    st.metric(T["average_revenue"], f"{result['kpis'].get('average_revenue', 0):,.2f}")


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    T["overview_tab"],
    T["products_tab"],
    T["customers_tab"],
    T["regions_tab"],
])

with tab1:
    summary_col, preview_col = st.columns([1.15, 1])

    with summary_col:
        st.subheader(T["summary"])
        if st.button(T["generate_summary"]):
            with st.spinner(T["summary_loading"]):
                try:
                    st.session_state.ai_summary = generate_ai_summary(result, brand_context, lang)
                except Exception as exc:
                    st.session_state.ai_summary = f"Error: {exc}"

        if st.session_state.ai_summary:
            st.markdown(st.session_state.ai_summary)
        else:
            st.markdown(f"<div class='ari-card-soft'>{T['ari_intro']}</div>", unsafe_allow_html=True)

    with preview_col:
        st.subheader(T["preview"])
        st.dataframe(df.head(10), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader(T["quick_insights"])
        for item in result["rule_based_insights"]:
            st.info(item)
    with c2:
        st.subheader(T["quick_actions"])
        for item in result["rule_based_recommendations"]:
            st.success(item)

    st.subheader(T["trend"])
    if result["trend"] is not None:
        trend_df = result["trend"].copy()
        x_col = trend_df.columns[0]
        st.plotly_chart(plot_line(trend_df, x_col), use_container_width=True)
    else:
        st.info(T["no_chart"])

with tab2:
    left, right = st.columns(2)
    with left:
        st.subheader(T["top_products"])
        if result["top_products"] is not None:
            top_df = result["top_products"].copy()
            label_col = top_df.columns[0]
            st.plotly_chart(plot_bar(top_df, label_col), use_container_width=True)
            st.dataframe(top_df, use_container_width=True)
        else:
            st.info(T["no_chart"])

    with right:
        st.subheader(T["bottom_products"])
        if result["bottom_products"] is not None:
            bottom_df = result["bottom_products"].copy()
            label_col = bottom_df.columns[0]
            st.plotly_chart(plot_bar(bottom_df, label_col), use_container_width=True)
            st.dataframe(bottom_df, use_container_width=True)
        else:
            st.info(T["no_chart"])

    st.subheader(T["category"])
    if result["category_breakdown"] is not None:
        cat_df = result["category_breakdown"].copy()
        label_col = cat_df.columns[0]
        st.plotly_chart(plot_bar(cat_df, label_col), use_container_width=True)
        st.dataframe(cat_df, use_container_width=True)
    else:
        st.info(T["no_chart"])

with tab3:
    st.subheader(T["customer"])
    if result["customer_breakdown"] is not None:
        cust_df = result["customer_breakdown"].copy()
        label_col = cust_df.columns[0]
        st.plotly_chart(plot_bar(cust_df, label_col), use_container_width=True)
        st.dataframe(cust_df, use_container_width=True)
    else:
        st.info(T["no_chart"])

with tab4:
    st.subheader(T["region"])
    if result["region_breakdown"] is not None:
        reg_df = result["region_breakdown"].copy()
        label_col = reg_df.columns[0]
        st.plotly_chart(plot_bar(reg_df, label_col), use_container_width=True)
        st.dataframe(reg_df, use_container_width=True)
    else:
        st.info(T["no_chart"])

    st.subheader(T["map"])
    st.caption(T["map_note"])
    if st.button(T["generate_map"]):
        with st.spinner(T["map_loading"]):
            region_col = result["detected_columns"]["region"]
            revenue_col = result["detected_columns"]["revenue"]
            order_col = result["detected_columns"]["order"]

            if region_col:
                map_working = df.copy()
                if revenue_col:
                    map_working["_rev"] = pd.to_numeric(map_working[revenue_col], errors="coerce")
                st.session_state.map_df = build_order_map(map_working, region_col, order_col, revenue_col)
            else:
                st.session_state.map_df = None

    if st.session_state.map_df is not None:
        import plotly.express as px

        map_df = st.session_state.map_df.copy()
        region_col = result["detected_columns"]["region"]
        fig = px.scatter_geo(
            map_df,
            lat="lat",
            lon="lon",
            size="orders",
            hover_name=region_col,
            hover_data={"orders": True, "revenue": True, "lat": False, "lon": False},
            projection="natural earth",
        )
        fig.update_layout(
            paper_bgcolor="white",
            font=dict(color="#111111", family="Inter"),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(T["no_map"])


# =========================================================
# CHAT WITH ARI
# =========================================================

st.markdown("---")
st.subheader(T["chat_title"])
if not st.session_state.chat_history:
    st.caption(T["chat_empty"])

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input(T["chat_placeholder"])
if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner(T["chat_loading"]):
            try:
                response = answer_chat_question(
                    user_question,
                    analysis_context,
                    st.session_state.chat_history,
                    brand_context,
                    lang,
                )
            except Exception as exc:
                response = f"Error: {exc}"
            st.markdown(response)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
