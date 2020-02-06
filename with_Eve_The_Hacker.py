#!/usr/bin/env python3
# coding: utf-8

import math
import matplotlib.pyplot as plt
import numpy as np

import qiskit
from qiskit import BasicAer, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from time import sleep

CRED    = '\033[31m'
CGREEN  = '\033[32m'
CYELLOW = '\033[33m'
CBLUE   = '\033[34m'
CVIOLET = '\033[35m'
CEND = '\033[0m'

print('')
print('')
print(CGREEN + "******" + CEND + CYELLOW + " Starting Quantum Program " + CEND + CGREEN + "******" + CEND )
print('')
print('')
mes = input( CVIOLET + "Enter your secret message: " + CYELLOW)
print('')
print('')

sleep(1)
n = len(mes)*3
nlist = []
for i in range(int(n/10)):
    nlist.append(10)
if n%10 != 0:
    nlist.append(n%10)

print(CGREEN + 'Initial key length: ' + CEND,n, flush = True)

def randomStringGen(string_length):
    output_list = []
    output = ''
    backend = BasicAer.get_backend('qasm_simulator')  
    circuits = ['rs']
    n = string_length
    temp_n = 10
    temp_output = ''
    for i in range(math.ceil(n/temp_n)):
        q = QuantumRegister(temp_n, name='q')
        c = ClassicalRegister(temp_n, name='c')
        rs = QuantumCircuit(q, c, name='rs')
        for i in range(temp_n):
            rs.h(q[i])
            rs.measure(q[i],c[i])
        result = execute(rs, backend, shots=1).result()
        counts = result.get_counts(rs)
        result_key = list(result.get_counts(rs).keys())
        temp_output = result_key[0]
        output += temp_output
    return output[:n]

key = randomStringGen(n)
print(CGREEN + 'Initial key: ' + CEND,key, flush = True)
print('')
print(CGREEN + "******" + CEND + CYELLOW + " generate random rotation strings for Alice and Bob " + CEND + CGREEN + "******" + CEND )
print('')

Alice_rotate = randomStringGen(n)
Bob_rotate = randomStringGen(n)
sleep(1)
print(CGREEN + "Alice's rotation string:" + CEND,Alice_rotate, flush = True)

sleep(2)
print(CYELLOW + "Bob's rotation string:  " + CEND ,Bob_rotate, flush = True)

#start up your quantum program
print('')
print(CGREEN + "******" + CEND + CYELLOW + " Starting up " + CEND + CGREEN + "******" + CEND )
print('')

backend = BasicAer.get_backend('qasm_simulator')  
shots = 1
circuits = ['send_over']
Bob_result = ''

for ind,l in enumerate(nlist):
    if l < 10:
        key_temp = key[10*ind:10*ind+l]
        Ar_temp = Alice_rotate[10*ind:10*ind+l]
        Br_temp = Bob_rotate[10*ind:10*ind+l]
    else:
        key_temp = key[l*ind:l*(ind+1)]
        Ar_temp = Alice_rotate[l*ind:l*(ind+1)]
        Br_temp = Bob_rotate[l*ind:l*(ind+1)]
    
    #start up the rest of your quantum circuit information
    q = QuantumRegister(l, name='q')
    c = ClassicalRegister(l, name='c')
    send_over = QuantumCircuit(q, c, name='send_over')
    for i,j,k,n in zip(key_temp,Ar_temp,Br_temp,range(0,len(key_temp))):
        i = int(i)
        j = int(j)
        k = int(k)
        if i > 0:
            send_over.x(q[n])
        if j > 0:
            send_over.h(q[n])
        if k > 0:
            send_over.h(q[n])
        send_over.measure(q[n],c[n])
    result_so = execute([send_over], backend, shots=shots).result()
    counts_so = result_so.get_counts(send_over)
    result_key_so = list(result_so.get_counts(send_over).keys())
    Bob_result += result_key_so[0][::-1]
sleep(2)
print(CYELLOW + "Bob's results: " + CEND, Bob_result, flush = True)

def makeKey(rotation1,rotation2,results):
    key = ''
    count = 0
    for i,j in zip(rotation1,rotation2):
        if i == j:
            key += results[count]
        count += 1
    return key
  
Akey = makeKey(Bob_rotate,Alice_rotate,key)
Bkey = makeKey(Bob_rotate,Alice_rotate,Bob_result)

sleep(2)

print(CGREEN + "Alice's key:" + CEND,Akey, flush = True)
print(CYELLOW + "Bob's key:  " + CEND,Bkey, flush = True)
shortened_Akey = Akey[:len(mes)]
encoded_m=''
print('')
print(CGREEN + "******" + CEND + CYELLOW + " Encrypting the message using encryption key" + CEND + CGREEN + "******" + CEND )
print('')

for m,k in zip(mes,shortened_Akey):
    encoded_c = chr(ord(m) + 2*ord(k) % 256)
    encoded_m += encoded_c
sleep(2)
print( CGREEN +'encoded message:  ' + CEND,encoded_m.encode("utf-8"), flush = True)
shortened_Bkey = Bkey[:len(mes)]

print('')
print(CGREEN + "******" + CEND + CYELLOW + "Decrypting the message " + CEND + CGREEN + "******" + CEND )
print('')print('')
print(CGREEN + "******" + CEND + CYELLOW + "Message received by Bob " + CEND + CGREEN + "******" + CEND )
print('')
sleep(2)
result = ''
for m,k in zip(encoded_m,shortened_Bkey):
    encoded_c = chr(ord(m) - 2*ord(k) % 256)
    result += encoded_c
sleep(2)
print(CYELLOW + 'recovered message:' + CEND, result, flush = True)

print('')
print(CGREEN + "******" + CEND + CYELLOW + "Simulating the same program with Eve -The Hacker present" + CEND + CGREEN + "******" + CEND )
print('')

backend = BasicAer.get_backend('qasm_simulator')  
shots = 1
circuits = ['Eve']

Eve_result = ''
for ind,l in enumerate(nlist):
    if l < 10:
        key_temp = key[10*ind:10*ind+l]
        Ar_temp = Alice_rotate[10*ind:10*ind+l]
    else:
        key_temp = key[l*ind:l*(ind+1)]
        Ar_temp = Alice_rotate[l*ind:l*(ind+1)]

    q = QuantumRegister(l, name='q')
    c = ClassicalRegister(l, name='c')
    Eve = QuantumCircuit(q, c, name='Eve')
    for i,j,n in zip(key_temp,Ar_temp,range(0,len(key_temp))):
        i = int(i)
        j = int(j)
        if i > 0:
            Eve.x(q[n])
        if j > 0:
            Eve.h(q[n])
        Eve.measure(q[n],c[n])
    result_eve = execute(Eve, backend, shots=shots).result()
    counts_eve = result_eve.get_counts()
    result_key_eve = list(result_eve.get_counts().keys())
    Eve_result += result_key_eve[0][::-1]

print(CRED + "Eve's results: " + CEND, Eve_result, flush = True)
backend = BasicAer.get_backend('qasm_simulator')  
shots = 1
circuits = ['Eve2']

Bob_badresult = ''
for ind,l in enumerate(nlist):
    if l < 10:
        key_temp = key[10*ind:10*ind+l]
        Eve_temp = Eve_result[10*ind:10*ind+l]
        Br_temp = Bob_rotate[10*ind:10*ind+l]
    else:
        key_temp = key[l*ind:l*(ind+1)]
        Eve_temp = Eve_result[l*ind:l*(ind+1)]
        Br_temp = Bob_rotate[l*ind:l*(ind+1)]
    
    q = QuantumRegister(l, name='q')
    c = ClassicalRegister(l, name='c')
    Eve2 = QuantumCircuit(q , c, name='Eve2')
    
    #prepare qubits
    for i,j,n in zip(Eve_temp,Br_temp,range(0,len(key_temp))):
        i = int(i)
        j = int(j)
        if i > 0:
            Eve2.x(q[n])
        if j > 0:
            Eve2.h(q[n])
        Eve2.measure(q[n],c[n])
    
    #execute
    result_eve = execute(Eve2, backend, shots=shots).result()
    counts_eve = result_eve.get_counts()
    result_key_eve = list(result_eve.get_counts().keys())
    Bob_badresult += result_key_eve[0][::-1]

sleep(2)
print(CYELLOW + "Bob's previous results (w/o Eve):" + CEND ,Bob_result, flush = True)
print(CRED + "Bob's results from Eve:\t\t " + CEND ,Bob_badresult, flush = True)

print('')
print(CGREEN + "******" + CEND + CYELLOW + "Making fake keys for Bob by Eve" + CEND + CGREEN + "******" + CEND )
print('')

Akey = makeKey(Bob_rotate,Alice_rotate,key)
Bkey = makeKey(Bob_rotate,Alice_rotate,Bob_badresult)
print(CGREEN + "Alice's key:   " + CEND ,Akey, flush = True)
print(CYELLOW + "Bob's key:     " + CEND ,Bkey, flush = True)

check_key = randomStringGen(len(Akey))
print(CYELLOW + 'spots to check:' + CEND,check_key, flush = True)

Alice_keyrotate = makeKey(Bob_rotate,Alice_rotate,Alice_rotate)
Bob_keyrotate = makeKey(Bob_rotate,Alice_rotate,Bob_rotate)

sleep(1)

print('')
print(CGREEN + "******" + CEND + CYELLOW + "Detecting the presence of Eve" + CEND + CGREEN + "******" + CEND )
print('')
sub_Akey = ''
sub_Arotate = ''
count = 0
for i,j in zip(Alice_rotate,Akey):
    if int(check_key[count]) == 1:
        sub_Akey += Akey[count]
        sub_Arotate += Alice_keyrotate[count]
    count += 1

sub_Bkey = ''
sub_Brotate = ''
count = 0
for i,j in zip(Bob_rotate,Bkey):
    if int(check_key[count]) == 1:
        sub_Bkey += Bkey[count]
        sub_Brotate += Bob_keyrotate[count]
    count += 1
sleep(3)
print(CGREEN + "subset of Alice's key:" + CEND ,sub_Akey, flush = True)
print(CYELLOW + "subset of Bob's key:  " + CEND, sub_Bkey, flush = True)

print('')
print('')

print('')
print(CGREEN + "******" + CEND + CYELLOW + "Comparing Alice and Bob's key subsets " + CEND + CGREEN + "******" + CEND )
print('')
secure = True
sleep(5)
for i,j in zip(sub_Akey,sub_Bkey):
    if i == j:
        secure = True
    else:
        secure = False
        break;
if not secure:
    print( CRED + 'Eve - The Hacker detected! Be Careful.' + CEND , flush = True)
else:
    print(CRED + 'Eve escaped detection!' + CEND, flush = True)

if secure:
    new_Akey = ''
    new_Bkey = ''
    for index,i in enumerate(check_key):
        if int(i) == 0:
            new_Akey += Akey[index]
            new_Bkey += Bkey[index]
    print( CVIOLET + 'new A and B keys: ' + CEND ,new_Akey,new_Bkey, flush = True)
    if(len(mes)>len(new_Akey)):
        print( CVIOLET +'Your new key is not long enough.' + CEND , flush = True)

sleep(1)
print('')
print('')
print(CGREEN + "******" + CEND + CYELLOW + " Ending Quantum Program !! Thank you!! " + CEND + CGREEN + "******" + CEND , flush = True)
sleep(1)

