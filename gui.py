from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Radiobutton, StringVar
from tkinter import messagebox
import os
from threading import Thread
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class TubeRevoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('TubeRevo 2')
        self.master.geometry('900x540')
        self.master.configure(bg="#435B47")
        self.master.resizable(width=False, height=False)

        self.load_images()
        self.create_widgets()

    def load_images(self):
        # Carregamento das imagens
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))

        self.image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))

        self.image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))

        self.image_image_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))

    def create_widgets(self):
        self.canvas = Canvas(
            self.master,
            bg="#435B47",
            height=540,
            width=900,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            450.0,
            365.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=117.5,
            y=344.0,
            width=665.0,
            height=41.0
        )

        # Adicione as imagens ao canvas
        self.image_1 = self.canvas.create_image(
            451.0,
            289.0,
            image=self.image_image_1
        )

        self.image_2 = self.canvas.create_image(
            224.0,
            193.0,
            image=self.image_image_2
        )

        self.image_3 = self.canvas.create_image(
            675.0,
            190.0,
            image=self.image_image_3
        )

        self.image_4 = self.canvas.create_image(
            450.0,
            193.0,
            image=self.image_image_4
        )

        self.canvas.create_text(
            194.0,
            20.0,
            anchor="nw",
            text="PAZ ENTRE AS QUEBRADAS, GUERRA AOS SENHORES!",
            fill="#09A223",
            font=("WorkSans Bold", 20 * -1)
        )

        self.canvas.create_text(
            216.0,
            347.0,
            anchor="nw",
            text="Insira URL válida do youtube.",
            fill="#000000",
            font=("WorkSans Bold", 34 * -1)
        )

        self.radio_var = StringVar()
        self.radio_var.set("mp3")

        mp3_button = Radiobutton(self.master, text="MP3", variable=self.radio_var, value="mp3", command=self.update_status)
        mp3_button.place(x=197, y=414)

        wav_button = Radiobutton(self.master, text="WAV", variable=self.radio_var, value="wav", command=self.update_status)
        wav_button.place(x=332, y=414)

        mp4_button = Radiobutton(self.master, text="MP4", variable=self.radio_var, value="mp4", command=self.update_status)
        mp4_button.place(x=468, y=414)

        avi_button = Radiobutton(self.master, text="AVI", variable=self.radio_var, value="avi", command=self.update_status)
        avi_button.place(x=611, y=414)

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.download_video,
            relief="flat"
        )
        self.button_1.place(
            x=284.0,
            y=459.0,
            width=332.0,
            height=53.0
        )

        # Ajuste aqui para subir o título em 15 pixels
        self.status_label = Label(
            self.master,
            text="Aguardando",
            font=("Arial", 14),
            bg='#435B47',
            fg='#09A223'
        )
        self.status_label.place(x=400, y=512) 

    def download_video(self):
        url = self.entry_1.get()
        format_option = self.radio_var.get()  # Adicionado aqui

        if not url:
            messagebox.showerror("Erro", "Insira uma URL válida.")
            return

        download_path = str(Path.home() / "Desktop")

        try:
            yt = YouTube(url)

            if format_option == "mp3":
                audio_stream = yt.streams.filter(only_audio=True).first()
                self.download_stream(audio_stream, download_path, f"{yt.title}.mp3", format_option)  # Passado format_option aqui
            elif format_option == "mp4":
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
                self.download_stream(video_stream, download_path, f"{yt.title}.mp4", format_option)  # Passado format_option aqui
            elif format_option == "wav":
                audio_stream = yt.streams.filter(only_audio=True).first()
                self.download_stream(audio_stream, download_path, f"{yt.title}.wav", format_option)  # Passado format_option aqui
            elif format_option == "avi":
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
                self.download_stream(video_stream, download_path, f"{yt.title}.avi", format_option)  # Passado format_option aqui
            else:
                messagebox.showerror("Erro", "Formato não suportado.")

        except RegexMatchError:
            messagebox.showerror("Erro", "URL do YouTube inválida.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {str(e)}")

    def download_stream(self, stream, download_path, filename, format_option):
        if stream:
            self.status_label.config(text="Progresso: 0%")
            self.master.update()

            try:
                stream.download(download_path)

                original_filepath = os.path.join(download_path, stream.default_filename)
                converted_filepath = os.path.join(download_path, filename)

                if format_option == 'avi':
                    # Convertendo para AVI
                    video_clip = VideoFileClip(original_filepath)
                    video_clip.write_videofile(converted_filepath, codec='libx264', audio_codec='aac', threads=4, preset='ultrafast')
                    video_clip.close()
                    os.remove(original_filepath)
                else:
                    os.rename(original_filepath, converted_filepath)

                self.status_label.config(text="Download concluído!")
                self.master.after(10000, self.update_status)  # Volta para 'Aguardando' após 10 segundos

            except Exception as e:
                messagebox.showerror("Erro", f"Erro durante o download: {str(e)}")
                self.status_label.config(text="Aguardando")

        else:
            messagebox.showerror("Erro", f"Nenhuma stream encontrada para o formato {self.radio_var.get()}.")

    def update_status(self):
        self.status_label.config(text="Aguardando")


if __name__ == "__main__":
    root = Tk()
    app = TubeRevoGUI(root)
    root.mainloop()
