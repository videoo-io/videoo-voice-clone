import os
import nltk
import torch

from melo.api import TTS
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

output_dir = 'outputs_v2'
device = "cuda:0" if torch.cuda.is_available() else "cpu"

def download_nltk_resources():
    print("DOWNLOADING download_nltk_resources")
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger_eng')
    except LookupError:
        nltk.download('averaged_perceptron_tagger_eng')

def setup():
    download_nltk_resources()

tone_color_converter = None
def process(isload, text, language):
    if isload == True:
        print("LOADING tone_color_converter")
        ckpt_converter = 'checkpoints_v2/converter'

        tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

        os.makedirs(output_dir, exist_ok=True)

    print("PROCESSING tone_color_converter")
    reference_speaker = 'resources/example_reference.mp3' # This is the voice you want to clone
    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

    print("Audio Name : ", audio_name)

    src_path = f'{output_dir}/tmp.wav'

    # Speed is adjustable
    speed = 1.0

    model = TTS(language=language, device=device)
    speaker_ids = model.hps.data.spk2id    

    speaker_keys = speaker_ids.keys()

    print("SPEAKER_KEYS :" + str(list(speaker_keys)))

    speaker_id = list(speaker_ids.values())[0]
    speaker_key = list(speaker_ids.keys())[0]  # Safely convert dict_keys to a list and access the first element.
    speaker_key = speaker_key.lower().replace('_', '-')

    source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
    model.tts_to_file(text, speaker_id, src_path, speed=speed)
    save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

    # Run the tone color converter
    encode_message = "@MyShell"
    tone_color_converter.convert(
        audio_src_path=src_path, 
        src_se=source_se, 
        tgt_se=target_se, 
        output_path=save_path,
        message=encode_message)

    text_hint   = f'''Get response successfully \n'''
    speaker_wav = src_path

    return (text_hint, save_path, speaker_wav)

# setup()
# text_hint, save_path, speaker_wav = process(True, "hello world", "EN")
# text_hint, save_path, speaker_wav = process(False, "Je suis l'Etudiante a L'universite D'istanbul", "FR")