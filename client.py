from gradio_client import Client

client = Client("http://0.0.0.0:7860/")
result = client.predict(
	"Howdy are you doing!",	# str  in 'Text Prompt' Textbox component
	"en_default,en_default",	# str (Option from: [('en_default', 'en_default'), ('en_us', 'en_us'), ('en_br', 'en_br'), ('en_au', 'en_au'), ('en_in', 'en_in'), ('es_default', 'es_default'), ('fr_default', 'fr_default'), ('jp_default', 'jp_default'), ('zh_default', 'zh_default'), ('kr_default', 'kr_default')]) in 'Style' Dropdown component
	"https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",	# str (filepath on your computer (or URL) of file) in 'Reference Audio' Audio component
	True,	# bool  in 'Agree' Checkbox component
	fn_index=1
)
print(result)