import hashlib

def audio_hash(audio_path):
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    hash_object = hashlib.sha256()
    hash_object.update(audio_data)
    audio_hash = hash_object.hexdigest()
    
    return audio_hash[:10]

def str_to_hash(input_str):
    input_bytes = input_str.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(input_bytes)
    hash_code = hash_object.hexdigest()
    
    return hash_code[:10]

def get_unique_code(reference_speaker, text, language):
    return f"{audio_hash(reference_speaker)}_{str_to_hash(text)}_{language}"

if __name__ == '__main__':

    example_inputs = [
        {
            "text": "The bustling city square bustled with street performers, tourists, and local vendors.",
            "language": 'en_us',
            "reference_speaker": "/tmp/gradio/971e5614c2398ed64e7c476251ec42cdb699d033/speaker0-0-100.wav"
        },
        {
            "text": "Did you ever hear a folk tale about a giant turtle?",
            "language": 'en_us',
            "reference_speaker": "/tmp/gradio/971e5614c2398ed64e7c476251ec42cdb699d033/speaker0-0-100.wav"
        },
        {
            "text": "El resplandor del sol acaricia las olas, pintando el cielo con una paleta deslumbrante.",
            "language": 'es_default',
            "reference_speaker": "/tmp/gradio/aee184926eca7bb464419ac1e8052907928c68fa/speaker1-0-100.wav",
        },
        {
            "text": "我最近在学习machine learning，希望能够在未来的artificial intelligence领域有所建树。",
            "language": 'zh_default',
            "reference_speaker": "/tmp/gradio/8373380c451c716ded54e6d1de959cc7c5fc4d72/speaker2-0-100.wav",
        },
        {
            "text": "彼は毎朝ジョギングをして体を健康に保っています。",
            "language": 'jp_default',
            "reference_speaker": "/tmp/gradio/5faad1507b5d6bc61a39ca3184db5a7b554a7479/speaker3-0-100.wav",
        }
    ]

    for example_input in example_inputs:
        print(get_unique_code(example_input['reference_speaker'], example_input['text'], example_input['language']))

