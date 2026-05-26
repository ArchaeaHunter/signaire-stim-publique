import argparse
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os


def load_clean_csv(csv_path):
    """
    Load the csv table and returns the cleaned dataframe

    Parameters :
    ------------
    csv_path : path to the csv file

    Output :
    --------
    df : cleaned dataframe from csv
    """

    df = pd.read_csv("data/database_without_names.csv", header=1)
    df = df.drop(["Unnamed: 16", "Unnamed: 17", "Unnamed: 24"], axis=1)
    df = df[~df["Lien YouTube"].isna()]

    return df


def plot_treemap_domains_subdomains(df, save_dir):
    """
    Plot the treemap by domains and sub-domains.

    Parameters :
    ------------
    df : input dataframe containing the data
    save_dir : directory to save the plot
    """

    dom = df.groupby(["Domaine", "Sous-domaine"])["N°ID"].count().reset_index()
    dom["N°ID"] = pd.to_numeric(dom["N°ID"])

    n_colors = len(set(dom["Domaine"]))
    color_scale = px.colors.sample_colorscale(
        "oranges", [n / (n_colors - 1) for n in range(n_colors)]
    )
    fig = px.treemap(
        dom,
        values="N°ID",
        path=["Domaine", "Sous-domaine"],
        color_discrete_sequence=color_scale,
        title="Répartition du signaire par domaines et sous-domaines",
        width=1500,
        height=1000,
    )
    fig.update_traces(
        marker=dict(cornerradius=5),
        root_color="#112760",
        texttemplate="<b>%{label}</b><br>%{value}",
        branchvalues="total",
        textinfo="label+value",
        textfont_size=25,
    )
    fig.update_layout(
        margin=dict(t=60, l=25, r=25, b=25),
        paper_bgcolor="#112760",
        plot_bgcolor="#112760",
        title=dict(
            text="Répartition du signaire par domaines et sous-domaines",
            y=0.98,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=45, color="white"),
        ),
    )

    fig.write_html(
        os.path.join(save_dir, "treemap_domains.html"),
        full_html=False,
        include_plotlyjs="cdn",
    )
    fig.write_image(os.path.join(save_dir, "treemap_domains.svg"))


def plot_cumsum_dates(df, save_dir):
    """
    Plot the graph with the cumulative sum of lexic by creation date.

    Parameters :
    ------------
    df : input dataframe containing the data
    save_dir : directory to save the plot
    """

    df.loc[df["Date"] == "29/02/2022", "Date"] = "28/02/2022"
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df.sort_values("Date")
    df["Année"] = df["Date"].dt.year
    dates = df.groupby(["Date"])["N°ID"].count().reset_index()
    dates["cumsum"] = dates["N°ID"].cumsum()

    fig = px.line(
        dates,
        x="Date",
        y="cumsum",
        title="Evolution du nombre de signes au cours du temps",
        width=1500,
        height=1000,
    )

    fig.update_layout(
        margin=dict(t=60, l=25, r=25, b=25),
        paper_bgcolor="#112760",
        plot_bgcolor="#112760",
        xaxis_title=dict(font=dict(size=20, color="white")),
        yaxis_title=dict(text="Somme cumulée", font=dict(size=20, color="white")),
        xaxis=dict(tickfont=dict(size=16, color="white")),
        yaxis=dict(tickfont=dict(size=16, color="white")),
        title=dict(
            text="Evolution du nombre de signes au cours du temps",
            y=0.98,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=25, color="white"),
        ),
    )

    fig.update_traces(line_color="#FF7011", line_width=5)

    fig.write_html(
        os.path.join(save_dir, "signes_au_cours_du_temps.html"),
        full_html=False,
        include_plotlyjs="cdn",
    )
    fig.write_image(os.path.join(save_dir, "signes_au_cours_du_temps.svg"))


def plot_treemap_domain_year(df, save_dir):
    """
    Plot the treemap by domain then year of creation

    Parameters :
    ------------
    df : input dataframe containing the data
    save_dir : directory to save the plot
    """

    dom_pers = df.groupby(["Domaine", "Année"])["N°ID"].count().reset_index()
    dom_pers = dom_pers.sort_values(["Domaine", "Année"], ascending=True)

    dom_pers["N°ID"] = pd.to_numeric(dom_pers["N°ID"])
    n_colors = len(set(dom_pers["Domaine"]))
    color_scale = px.colors.sample_colorscale(
        "oranges", [n / (n_colors - 1) for n in range(n_colors)]
    )
    fig = px.treemap(
        dom_pers,
        values="N°ID",
        path=["Domaine", "Année"],
        color_discrete_sequence=color_scale,
        title="Répartition du signaire par domaines et année de création",
        width=1500,
        height=1000,
    )
    fig.update_traces(
        marker=dict(cornerradius=5),
        root_color="#112760",
        texttemplate="<b>%{label}</b><br>%{value}",
        branchvalues="total",
        textinfo="label+value",
        textfont_size=25,
    )
    fig.update_layout(
        margin=dict(t=60, l=25, r=25, b=25),
        paper_bgcolor="#112760",
        plot_bgcolor="#112760",
        title=dict(
            text="Répartition du signaire par domaines et année de création",
            y=0.98,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=45, color="white"),
        ),
    )

    fig.data[0].textinfo = "label+text+value"
    fig.write_html(
        os.path.join(save_dir, "treemap_domains_annee.html"),
        full_html=False,
        include_plotlyjs="cdn",
    )
    fig.write_image(os.path.join(save_dir, "treemap_domains_annee.svg"))


def plot_treemap_year_domain(df, save_dir):
    """
    Plot the treemap by year of creation then domain

    Parameters :
    ------------
    df : input dataframe containing the data
    save_dir : directory to save the plot
    """
    dom_pers = df.groupby(["Domaine", "Année"])["N°ID"].count().reset_index()
    dom_pers = dom_pers.sort_values(["Domaine", "Année"], ascending=True)

    dom_pers = dom_pers.sort_values(["Année", "Domaine"], ascending=True)
    n_colors = len(set(dom_pers["Année"]))
    color_scale = px.colors.sample_colorscale(
        "oranges", [n / (n_colors - 1) for n in range(n_colors)]
    )
    fig = px.treemap(
        dom_pers,
        values="N°ID",
        path=["Année", "Domaine"],
        color_discrete_sequence=color_scale,
        title="Répartition du signaire par domaines et année de création",
        width=1500,
        height=1000,
    )
    fig.update_traces(
        marker=dict(cornerradius=5),
        root_color="#112760",
        texttemplate="<b>%{label}</b><br>%{value}",
        branchvalues="total",
        textinfo="label+value",
        textfont_size=25,
    )
    fig.update_layout(
        margin=dict(t=60, l=25, r=25, b=25),
        paper_bgcolor="#112760",
        plot_bgcolor="#112760",
        title=dict(
            text="Répartition du signaire par domaines et année de création",
            y=0.98,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=45, color="white"),
        ),
    )

    fig.data[0].textinfo = "label+text+value"
    fig.write_html(
        os.path.join(save_dir, "treemap_annee_domains.html"),
        full_html=False,
        include_plotlyjs="cdn",
    )
    fig.write_image(os.path.join(save_dir, "treemap_annee_domains.svg"))


def main(csv_path, save_dir):
    """
    Main script to load csv and build all figures to have a great idea of the content

    Parameters :
    ------------
    csv_path : path to the csv file
    save_dir : directory to save plots
    """
    pio.get_chrome()

    df = load_clean_csv(csv_path)

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    plot_treemap_domains_subdomains(df, save_dir)
    plot_cumsum_dates(df, save_dir)
    plot_treemap_domain_year(df, save_dir)
    plot_treemap_year_domain(df, save_dir)


def parse_arguments():
    """
    Parse the input arguments from command line.
    Arguments to be parsed are :
    --csv : path to the csv file
    --dir : path to the directory to save figures

    Output :
    ---------
    parser.parse_args() : arguments parsed
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv", help="Path to the csv file")
    parser.add_argument("-d", "--dir", help="Path to the directory to save figures")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.csv, args.dir)
