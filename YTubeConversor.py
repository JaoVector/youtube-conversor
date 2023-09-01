from pytube import YouTube
from IPython.display import YouTubeVideo
from googleapiclient.discovery import build
from pytube.exceptions import VideoUnavailable
import os
import re as rex


youTubeApiKey="insira-chave-google-da-API-do-YouTube"
youtube = build('youtube', 'v3', developerKey=youTubeApiKey)
urls = []
rege = r"\w+[A-Za-z0-9-]+$"


def ConsultaIdVideos(playlistId: str):

    playlist_list_videos = []
    nextPageToken = None

    while True:
        resp = youtube.playlistItems().list(part='snippet', playlistId=playlistId, maxResults=100, pageToken=nextPageToken).execute()
        playlist_list_videos += resp['items']
        nextPageToken = resp.get('nextPageToken')

        if nextPageToken is None:
            break

    videos_id_list = list(map(lambda x: x['snippet']['resourceId']['videoId'], playlist_list_videos))
    
    videos_link_list = list(map(ConcatenaLinkId, videos_id_list))
    ConverteVideo(videos_link_list)


def ConverteVideo(urlList: list):

    dir = str(input("Digite o Dir para Guardar os Arquivos: "))

    for i in urlList:
        try:
            ytUrl = YouTube(url=i)
            video_audio = ytUrl.streams.filter(only_audio=True).first()
            arquivo = video_audio.download(output_path=dir)
            nome, ext = os.path.splitext(arquivo)
            arquivo_mp3 = nome + '.mp3'
            os.rename(arquivo, arquivo_mp3)
        except VideoUnavailable:
            continue
        

def RegexUrlPlayList(url: str):
    reg = rex.compile(rege)
    urlM = reg.findall(url)
    idPlay = urlM.pop()
    ConsultaIdVideos(idPlay)


def ConcatenaLinkId(idVideo):
    return "https://www.youtube.com/watch?v=" + idVideo


def Menu():
    print("====== Escolha uma Opção =======")
    print("=== 1 para Converter Video =====")
    print("=== 2 para Converter Playlist ==")
    print("================================")
    op = int(input("OP: "))
    os.system("cls")
    
    if op == 1:
        url = str(input("URL: "))
        urls.append(url)
        ConverteVideo(urls)
        print("Conversão Concluida Com Sucesso")
    elif op == 2:
        urlPlay = str(input("URL: "))
        RegexUrlPlayList(urlPlay)
        print("Conversão Concluida Com Sucesso")
    else:
        print("Opção invalida")
        os.system("cls")
        Menu()


Menu()