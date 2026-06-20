/* ==========================================================
   dashboard.js
   Componente React do dashboard — sem JSX, sem build step.
   Consome /api/dashboard e renderiza cards + gráficos.
   ========================================================== */

const { useState, useEffect } = React;
const {
  BarChart, Bar, PieChart, Pie, Cell, Tooltip,
  XAxis, YAxis, CartesianGrid, Legend, ResponsiveContainer
} = Recharts;

/* ---- Paleta de cores ---- */
const CORES_TIPO = {
  "Estoque Seco":       "#f59e0b",
  "Câmara Fria":        "#3b82f6",
  "Câmara Congelada":   "#06b6d4",
};
const CORES_BARRAS = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe",
                      "#818cf8", "#4f46e5", "#7c3aed", "#9333ea", "#a855f7"];

/* ---- Estilos inline (sem arquivo extra) ---- */
const s = {
  grid:       { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, marginBottom: 24 },
  card:       { background: "#fff", borderRadius: 8, padding: "16px 20px", boxShadow: "0 1px 3px rgba(0,0,0,.1)" },
  cardNum:    { fontSize: 32, fontWeight: 700, margin: "4px 0" },
  cardLabel:  { fontSize: 13, color: "#6b7280" },
  row:        { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 },
  rowFull:    { marginBottom: 24 },
  chartBox:   { background: "#fff", borderRadius: 8, padding: 16, boxShadow: "0 1px 3px rgba(0,0,0,.1)" },
  title:      { fontSize: 15, fontWeight: 600, marginBottom: 12, color: "#374151" },
  alertTable: { width: "100%", borderCollapse: "collapse", fontSize: 13 },
  alertTh:    { textAlign: "left", padding: "8px 12px", background: "#f9fafb", color: "#6b7280", borderBottom: "1px solid #e5e7eb" },
  alertTd:    { padding: "8px 12px", borderBottom: "1px solid #f3f4f6" },
  alertBadge: { background: "#fee2e2", color: "#b91c1c", borderRadius: 4, padding: "2px 8px", fontSize: 12, fontWeight: 600 },
  loading:    { padding: 40, textAlign: "center", color: "#6b7280" },
  empty:      { padding: 20, textAlign: "center", color: "#9ca3af", fontSize: 13 },
};

/* ---- Cards do topo ---- */
function Cards({ data }) {
  const items = [
    { label: "Insumos ativos",    valor: data.total_insumos,    cor: "#6366f1" },
    { label: "Produtos",          valor: data.total_produtos,   cor: "#10b981" },
    { label: "Vendas (30 dias)",  valor: data.vendas_mes,       cor: "#3b82f6" },
    { label: "⚠️ Alertas",        valor: data.alertas_estoque,  cor: "#ef4444" },
  ];
  return React.createElement("div", { style: s.grid },
    items.map(item =>
      React.createElement("div", { key: item.label, style: s.card },
        React.createElement("div", { style: { ...s.cardNum, color: item.cor } }, item.valor),
        React.createElement("div", { style: s.cardLabel }, item.label)
      )
    )
  );
}

/* ---- Gráfico de pizza — estoque por tipo ---- */
function GraficoEstoqueTipo({ data }) {
  if (!data.length) return React.createElement("div", { style: s.empty }, "Sem dados de estoque.");

  const renderLabel = ({ name, percent }) =>
    `${name} (${(percent * 100).toFixed(0)}%)`;

  return React.createElement("div", { style: s.chartBox },
    React.createElement("div", { style: s.title }, "📦 Estoque por Armazenamento"),
    React.createElement(ResponsiveContainer, { width: "100%", height: 260 },
      React.createElement(PieChart, null,
        React.createElement(Pie, {
          data: data,
          dataKey: "total",
          nameKey: "tipo",
          cx: "50%", cy: "50%",
          outerRadius: 90,
          label: renderLabel,
        },
          data.map(entry =>
            React.createElement(Cell, {
              key: entry.tipo,
              fill: CORES_TIPO[entry.tipo] || "#94a3b8"
            })
          )
        ),
        React.createElement(Tooltip, { formatter: (v) => [`${v} un`, "Total"] }),
        React.createElement(Legend)
      )
    )
  );
}

/* ---- Gráfico de barras — pratos mais vendidos ---- */
function GraficoPratos({ data }) {
  if (!data.length) return React.createElement("div", { style: s.empty }, "Nenhuma venda registrada nos últimos 30 dias.");

  return React.createElement("div", { style: s.chartBox },
    React.createElement("div", { style: s.title }, "🍽️ Pratos Mais Vendidos — Último Mês"),
    React.createElement(ResponsiveContainer, { width: "100%", height: 260 },
      React.createElement(BarChart, { data: data, margin: { top: 4, right: 16, left: 0, bottom: 40 } },
        React.createElement(CartesianGrid, { strokeDasharray: "3 3", stroke: "#f0f0f0" }),
        React.createElement(XAxis, {
          dataKey: "nome",
          tick: { fontSize: 11 },
          angle: -35,
          textAnchor: "end",
          interval: 0,
        }),
        React.createElement(YAxis, { tick: { fontSize: 11 }, allowDecimals: false }),
        React.createElement(Tooltip),
        React.createElement(Bar, { dataKey: "total", name: "Vendas", radius: [4, 4, 0, 0] },
          data.map((_, i) =>
            React.createElement(Cell, { key: i, fill: CORES_BARRAS[i % CORES_BARRAS.length] })
          )
        )
      )
    )
  );
}

/* ---- Tabela de alertas de compra ---- */
function TabelaAlertas({ data }) {
  return React.createElement("div", { style: s.chartBox },
    React.createElement("div", { style: s.title }, "🛒 Insumos para Comprar"),
    data.length === 0
      ? React.createElement("div", { style: s.empty }, "✅ Todos os insumos estão dentro do estoque mínimo.")
      : React.createElement("table", { style: s.alertTable },
          React.createElement("thead", null,
            React.createElement("tr", null,
              ["Insumo", "Armazenamento", "Atual", "Mínimo", "Falta"].map(h =>
                React.createElement("th", { key: h, style: s.alertTh }, h)
              )
            )
          ),
          React.createElement("tbody", null,
            data.map(item =>
              React.createElement("tr", { key: item.id },
                React.createElement("td", { style: s.alertTd }, item.nome),
                React.createElement("td", { style: s.alertTd }, item.tipo_armazenamento),
                React.createElement("td", { style: s.alertTd }, `${item.estoque_atual} ${item.unidade}`),
                React.createElement("td", { style: s.alertTd }, `${item.estoque_minimo} ${item.unidade}`),
                React.createElement("td", { style: s.alertTd },
                  React.createElement("span", { style: s.alertBadge },
                    `${(item.estoque_minimo - item.estoque_atual).toFixed(2)} ${item.unidade}`
                  )
                )
              )
            )
          )
        )
  );
}

/* ---- App principal ---- */
function Dashboard() {
  const [dados, setDados] = useState(null);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    fetch("/api/dashboard")
      .then(r => r.json())
      .then(setDados)
      .catch(() => setErro("Não foi possível carregar o dashboard."));
  }, []);

  if (erro)   return React.createElement("div", { style: { ...s.loading, color: "#ef4444" } }, erro);
  if (!dados) return React.createElement("div", { style: s.loading }, "Carregando dashboard...");

  return React.createElement("div", null,
    React.createElement("h1", { style: { marginBottom: 20 } }, "📊 Dashboard"),

    /* Cards */
    React.createElement(Cards, { data: dados.cards }),

    /* Linha: pizza + barras */
    React.createElement("div", { style: s.row },
      React.createElement(GraficoEstoqueTipo, { data: dados.estoque_por_tipo }),
      React.createElement(GraficoPratos,      { data: dados.pratos_mais_vendidos })
    ),

    /* Tabela de alertas */
    React.createElement("div", { style: s.rowFull },
      React.createElement(TabelaAlertas, { data: dados.insumos_abaixo_minimo })
    )
  );
}

/* ---- Monta no DOM ---- */
const root = ReactDOM.createRoot(document.getElementById("dashboard-root"));
root.render(React.createElement(Dashboard));