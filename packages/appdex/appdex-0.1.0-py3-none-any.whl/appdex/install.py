import subprocess

import typer

from appdex.config import tmp_dir, app_image_dir
from appdex.util import create_dir_if_not_exists

app = typer.Typer(no_args_is_help=True)

excluded_attributes = {
    "symbols": ["excluded_attributes", "app"],
    "imports": ["typer", "subprocess", "tmp_dir"],
}

@app.command()
def potato():
    typer.echo("potato")

@app.command()
def pipx():
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "pipx"])
    subprocess.run(["pipx", "ensurepath"])
    subprocess.run(["sudo", "pipx", "ensurepath", "--global"])


@app.command()
def zsh():
    subprocess.run(["sudo", "apt", "install", "zsh"])
    subprocess.run(["sh", "-c", "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"])
    subprocess.run(["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions", "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions"])

@app.command()
def kitty():
    subprocess.run(["curl", "-L", "https://sw.kovidgoyal.net/kitty/installer.sh", "|", "sh", "/dev/stdin"])
    subprocess.run(["ln", "-sf", "~/.local/kitty.app/bin/kitty", "~/.local/kitty.app/bin/kitten", "~/.local/bin/"])
    subprocess.run(["cp", "~/.local/kitty.app/share/applications/kitty.desktop", "~/.local/share/applications/"])
    subprocess.run(["cp", "~/.local/kitty.app/share/applications/kitty-open.desktop", "~/.local/share/applications/"])
    subprocess.run(["sed", "-i", "\"s|Icon=kitty|Icon=$(readlink -f ~)/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png|g\"", "~/.local/share/applications/kitty*.desktop"])
    subprocess.run(["sed", "-i", "\"s|Exec=kitty|Exec=$(readlink -f ~)/.local/kitty.app/bin/kitty|g\"", "~/.local/share/applications/kitty*.desktop"])
    subprocess.run(["echo", "'kitty.desktop' > ~/.config/xdg-terminals.list"])

@app.command()
def powerlevel10k():
    subprocess.run(["git", "clone", "--depth=1", "https://github.com/romkatv/powerlevel10k.git", "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"])
    subprocess.run(["p10k", "configure"])

@app.command()
def app_image_deps():
    subprocess.run(["sudo", "add-apt-repository", "universe"])
    subprocess.run(["sudo", "apt", "install", "libfuse2t64"])

@app.command()
def zen_browser():
    create_dir_if_not_exists(app_image_dir)
    file = f"{app_image_dir}/zen.AppImage"
    subprocess.run(["wget", "-O", file, "https://github.com/zen-browser/desktop/releases/download/1.0.0-a.35/zen-specific.AppImage"])
    subprocess.run(["chmod", "+x", file])

@app.command()
def proton_pass():
    file = f"{tmp_dir}/proton-pass.deb"
    subprocess.run(["wget", "-O", file, "https://proton.me/download/PassDesktop/linux/x64/ProtonPass_1.22.3.deb"])
    subprocess.run(["sudo", "dpkg", "-i", file])
    subprocess.run(["rm", file])

@app.command()
def jetbrains_toolbox():
    file = f"{tmp_dir}/jetbrains-toolbox.tar.gz"
    subprocess.run(["sudo", "apt", "install", "libfuse2"])
    subprocess.run(["wget", "-O", file, "https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.4.2.32922.tar.gz"])
    subprocess.run(["tar", "-xzf", file, "&&", f"{file}/jetbrains-toolbox"])
    subprocess.run(["rm", file])

@app.command()
def discord():
    file = f"{tmp_dir}/vencord.deb"
    subprocess.run(["wget", "-O", file, "https://vencord.dev/download/vesktop/amd64/deb"])
    subprocess.run(["sudo", "dpkg", "-i", file])
    subprocess.run(["rm", file])

@app.command()
def spotify():
    subprocess.run(["curl", "-sS", "https://download.spotify.com/debian/pubkey_6224F9941A8AA6D1.gpg", "|", "sudo", "gpg", "--dearmor", "--yes", "-o", "/etc/apt/trusted.gpg.d/spotify.gpg"])
    subprocess.run(["echo", "\"deb http://repository.spotify.com stable non-free\" |", "sudo", "tee", "/etc/apt/sources.list.d/spotify.list"])
    subprocess.run(["sudo", "apt-get", "update", "&&", "sudo", "apt-get", "install", "spotify-client"])

@app.command()
def session():
    file = f"{tmp_dir}/session.deb"
    subprocess.run(["wget", "-O", file, "'https://getsession.org/download?platform=linux&format=deb'"])
    subprocess.run(["sudo", "dpkg", "-i", file])
    subprocess.run(["rm", file])

@app.command()
def docker():
    subprocess.run(["sudo", "apt-get", "install", "ca-certificates", "curl"])
    subprocess.run(["sudo", "install", "-m", "0755", "-d", "/etc/apt/keyrings"])
    subprocess.run(["sudo", "curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg", "-o", "/etc/apt/keyrings/docker.asc"])
    subprocess.run(["sudo", "chmod", "a+r", "/etc/apt/keyrings/docker.asc"])
    subprocess.run(["echo", "\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable\" |", "sudo", "tee", "/etc/apt/sources.list.d/docker.list", ">", "/dev/null"])
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"])

@app.command()
def xclip():
    subprocess.run(["sudo", "apt-get", "install", "xclip"])

@app.command()
def oxen_repos():
    subprocess.run(["sudo", "curl", "-so", "/etc/apt/trusted.gpg.d/oxen.gpg", "https://deb.oxen.io/pub.gpg"])
    subprocess.run(["echo", "\"deb https://deb.oxen.io $(lsb_release -sc) main\" |", "sudo", "tee", "/etc/apt/sources.list.d/oxen.list"])
    subprocess.run(["sudo", "apt", "update"])

@app.command()
def build_essentials():
    subprocess.run(["sudo", "apt-get", "install", "build-essential"])

@app.command()
def cmake():
    subprocess.run(["sudo", "apt", "install", "cmake"])

#
# @app.command()
# def app(name: str = typer.Argument("...", help="App to install")):
#     """
#     Installs an app.
#     """
#     typer.echo(f"Installing {name}")
#     match name:
#         case "zsh":
#             zsh()
#         case "kitty":
#             kitty()
#         case "powerlevel10k":
#             powerlevel10k()
#         case "app_image_deps":
#             app_image_deps()
#         case "zen_browser":
#             zen_browser()
#         case "proton_pass":
#             proton_pass()
#         case "jetbrains_toolbox":
#             jetbrains_toolbox()
#         case "discord":
#             discord()
#         case "spotify":
#             spotify()
#         case "session":
#             session()
#         case "docker":
#             docker()
#         case "xclip":
#             xclip()
#         case "oxen_repos":
#             oxen_repos()
#         case "build_essentials":
#             build_essentials()
#         case "cmake":
#             cmake()
#         case _:
#             typer.echo(f"Invalid option: {name}")
#             typer.echo("Valid options are: " + ", ".join(options))
#             raise typer.Exit(code=1)


if __name__ == "__main__":
    app()