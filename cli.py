import argparse
import sys

from sentiment_app import __version__


def predire(args: argparse.Namespace) -> int:
    from api.model import predict  # import tardif : évite de charger le modèle pour --version
    texte = " ".join(args.texte)
    resultat = predict(texte)
    print(resultat)  # {"label": "POSITIVE", "score": 0.777, ...}
    return 0


def servir(_args: argparse.Namespace) -> int:
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000)
    return 0


def interface(_args: argparse.Namespace) -> int:
    import subprocess
    return subprocess.call(["streamlit", "run", "ui/app.py"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sentiment", description="Sentiment-app CLI")
    parser.add_argument("--version", action="version", version=f"sentiment-app {__version__}")

    commandes = parser.add_subparsers(dest="commande", required=True)

    p_predict = commandes.add_parser("predict", help="classe un avis, sans serveur")
    p_predict.add_argument("texte", nargs="+", help="l'avis à analyser")
    p_predict.set_defaults(fonction=predire)

    p_serve = commandes.add_parser("serve", help="lance l'API")
    p_serve.set_defaults(fonction=servir)

    p_ui = commandes.add_parser("ui", help="lance la page Streamlit")
    p_ui.set_defaults(fonction=interface)

    args = parser.parse_args(argv)
    return int(args.fonction(args))


if __name__ == "__main__":
    sys.exit(main())