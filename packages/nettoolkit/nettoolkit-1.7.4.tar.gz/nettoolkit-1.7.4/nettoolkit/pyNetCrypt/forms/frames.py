
from nettoolkit.nettoolkit.forms.formitems import *

# ============================ [ Juniper ] ======================================= #

def netcrypt_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('File Password Masking/Decryption', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Configuration file:',  text_color="black"), 
		 sg.InputText(key='netcrypt_file'), sg.FileBrowse()],
		[sg.Text('\t'),
		 sg.Button("Decrypt Passwords", size=(20,1),  change_submits=True, key='netcrypt_file_dec_btn_start', button_color="blue"),
		 sg.Button("Mask Passwords", size=(20,1),  change_submits=True, key='netcrypt_file_mask_btn_start', button_color="blue")],
		[sg.Text('\t'),
		 sg.Button("Generate MD5 Hex", size=(20,1),  change_submits=True, key='netcrypt_file_hash_btn_start', button_color="blue"),],

		under_line(80),

		[sg.Text('Password Encryption/Decryption', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Password string:', text_color="black"), sg.InputText(key='netcrypt_input_pw'), ],
		[sg.Text('\t'),
		 sg.Button("Cisco Encrypt", change_submits=True, key='netcrypt_cisco_enc_btn_start', button_color="blue"),
		 sg.Button("Cisco Decrypt", change_submits=True, key='netcrypt_cisco_dec_btn_start', button_color="blue"),],
		[sg.Text('\t'),
		 sg.Button("Juniper Encrypt", change_submits=True, key='netcrypt_juniper_enc_btn_start', button_color="blue"),
		 sg.Button("Juniper Decrypt", change_submits=True, key='netcrypt_juniper_dec_btn_start', button_color="blue"),],
		under_line(80),
		[sg.Text('Result:',  text_color="black"), sg.InputText(key='netcrypt_output_pw', disabled=True), ],
		under_line(80),



		])

# ========================================================================
CRYPT_FRAMES = {
	'Cryptology': netcrypt_frame(),
}