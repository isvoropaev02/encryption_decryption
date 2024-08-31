import numpy as np
from configuration import *

class Encryptor:
    def __init__(self, config) -> None:
        self._alphabet_len = config['alphabet_len']
        self._cycle_len = config['cycle_len']
        if config['codebook_source'] == 'new':
            self._codebook = self.generate_codebook(config)
            if config['save_new_codebook']:
                np.savetxt('codebook.txt', np.array(self._codebook), delimiter='\t', fmt='%i')
        elif config['codebook_source'] == 'file':
            self._codebook = np.loadtxt('codebook.txt', delimiter='\t', dtype=int)

    @classmethod
    def generate_codebook(cls, config):
        return np.random.randint(low=0, high=config['alphabet_len']-1, size=config['cycle_len'])
    
    def __check_message_format(self, mes) -> bool:
        for ii in range(len(mes)):
            if (mes[ii] != ' '):
                temp_val = ord(mes[ii])-ord('A')
                if (temp_val < 0 or temp_val>= self._alphabet_len):
                    return False
        return True
    
    def encrypt_message(self, mes) -> str:
        if self.__check_message_format(mes):
            ref_num=ord('A')
            en_message = list(mes)
            key_num = 0
            for ii in range(len(en_message)):
                if en_message[ii] != ' ':
                    en_message[ii] = chr(ref_num+(ord(en_message[ii])-ref_num + self._codebook[key_num]) % self._alphabet_len)
                    key_num = (key_num+1) % self._cycle_len
            
            return ''.join(en_message)
        else:
            raise(ValueError('Not acceptable characters (should be upercase or spaces)'))
    
    def decrypt_message(self, en_mes) -> str:
        ref_num=ord('A')
        message = list(en_mes)
        key_num = 0
        for ii in range(len(message)):
            if message[ii] != ' ':
                message[ii] = chr(ref_num+(ord(message[ii])-ref_num - self._codebook[key_num]) % self._alphabet_len)
                key_num = (key_num+1) % self._cycle_len
        
        return ''.join(message)