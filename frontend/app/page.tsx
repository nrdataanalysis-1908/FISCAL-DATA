"use client";

import { useEffect, useState } from "react";

type Summary = {
  gross_revenue: string;
  net_revenue: string;
  net_income: string;
  net_margin_percent: string;
  transaction_count: number;
};

type Dre = { rows: { label: string; amount: string }[]; note: string };

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const currency = (value: string) =>
  Number(value).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export default function Dashboard() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [dre, setDre] = useState<Dre | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/v1/dashboard/summary?period=2026-10`).then((r) => {
        if (!r.ok) throw new Error("Não foi possível carregar os indicadores.");
        return r.json();
      }),
      fetch(`${API}/api/v1/dre?period=2026-10`).then((r) => {
        if (!r.ok) throw new Error("Não foi possível carregar a DRE.");
        return r.json();
      }),
    ])
      .then(([s, d]) => { setSummary(s); setDre(d); })
      .catch((e: Error) => setError(e.message));
  }, []);

  const kpis = [
    ["Receita bruta", summary ? currency(summary.gross_revenue) : "—"],
    ["Receita líquida", summary ? currency(summary.net_revenue) : "—"],
    ["Lucro líquido gerencial", summary ? currency(summary.net_income) : "—"],
    ["Margem líquida", summary ? `${Number(summary.net_margin_percent).toLocaleString("pt-BR")}%` : "—"],
  ];

  return (
    <main>
      <header>
        <div>
          <div className="brand">NR FISCAL INTELLIGENCE</div>
          <div className="muted">NR TECH LAB · FISCAL & FINANCIAL DATA</div>
        </div>
        <span className="pill">DADOS SIMULADOS · OUT/2026</span>
      </header>

      <h1>Visão geral</h1>
      <p className="muted">NR Tech Store · empresa fictícia de comércio</p>
      {error && <div className="card">{error} Verifique se a API e o banco estão ativos.</div>}

      <section className="grid section">
        {kpis.map(([label, value]) => (
          <article className="card" key={label}>
            <div className="label">{label}</div>
            <div className="value">{value}</div>
          </article>
        ))}
      </section>

      <section className="card section">
        <h2>DRE gerencial</h2>
        {dre ? (
          <table>
            <thead><tr><th>Descrição</th><th>Valor</th></tr></thead>
            <tbody>
              {dre.rows.map((row, index) => (
                <tr key={row.label}>
                  <td style={{ fontWeight: [2, 4, 6, 10].includes(index) ? 700 : 400 }}>{row.label}</td>
                  <td>{currency(row.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p className="muted">Carregando demonstrativo...</p>}
        <p className="muted">{dre?.note}</p>
      </section>

      <section className="grid section">
        <article className="card">
          <div className="label">Cenário tributário</div>
          <h3>Simples Nacional</h3>
          <p className="muted">Integração com motor oficial em etapa posterior.</p>
          <span className="pill">Planejado</span>
        </article>
        <article className="card">
          <div className="label">Cenário tributário</div>
          <h3>Regime Regular</h3>
          <p className="muted">Integração com motor oficial em etapa posterior.</p>
          <span className="pill">Planejado</span>
        </article>
        <article className="card">
          <div className="label">Movimentações no período</div>
          <div className="value">{summary?.transaction_count ?? "—"}</div>
        </article>
        <article className="card">
          <div className="label">Governança</div>
          <h3>Rastreabilidade prevista</h3>
          <p className="muted">Origem, período, classificação e versão dos cálculos.</p>
        </article>
      </section>

      <p className="notice section">
        Protótipo educacional com dados fictícios. Os valores não representam apuração fiscal,
        escrituração contábil ou orientação tributária oficial.
      </p>
    </main>
  );
}
