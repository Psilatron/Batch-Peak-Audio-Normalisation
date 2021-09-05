
import numpy as np
import soundfile as sf
import time, os, sys, tkinter, tkinter.filedialog

#--------------------------------

def SelectDir(): #Directory selection GUI function.
    '''function to enable selection of directory by user input'''
    
    root = tkinter.Tk()
    root.wm_attributes("-topmost", 1)##Will display window on top of others
    root.withdraw()
    initialPath = os.getcwd()
    dirname = tkinter.filedialog.askdirectory(parent=root, initialdir=initialPath, title='Pick a directory')
    root.update() 
    
    if dirname == '':
        print("Selection Cancelled")
        sys.exit(1)
    root.destroy()
    return dirname

def ChannelCount(inputaudio):
  
    x=0;
    c_count=0
    
    monocheck=np.ndim(inputaudio)
    
    if monocheck == 1:
        c_count=1
    elif monocheck>1:
        for x in inputaudio[x]:
            c_count=c_count+1
    return(c_count)


def MonoNorm (inputfile,PkDbInput): # (input file name, Desired Peak Db Value)

    MonoPkVal=0
    silentflag=0
    [AudioIn,fs]=sf.read(inputfile)
    mono=AudioIn

    PkNormVal=0.0
    MonoNormalised=0
    PkNormVal=np.power(10,PkDb/20) #convert dB input value  


    silentflag = np.all((mono == 0)) #check if track consists of entirely 0s, i.e. silent track.
    if silentflag==1:
        #Detection of silent mono track. Will ouput input track as dummy.

        return(mono,fs,silentflag)
    
    MonoPkVal=np.max(np.abs(mono)) #maximum absoslute value of audio file amplitude
    #Normalization calculation
    MonoNormalised=mono*(PkNormVal/MonoPkVal)

    return(MonoNormalised,fs,silentflag)

def StereoNorm (inputfile,PkDbInput): # (input file name, Desired Peak Db Value)
    # The stereo audio file be normalised by using the peak value taken from 
    # channel with the highest peak as a reference. That means that if 
    # the one channel has a lower peak than the other this difference will
    # be preserved and scaled accordingly.

    [AudioIn,fs]=sf.read(inputfile)
    maxCh=0 #variable used to detect channel with highest peak level
    ChL=ChR=0
    PkNormVal=0.0
    maxL=maxR=0
    silentflag=0 #used to detect completely silent tracks
    
    silentflagL=0
    silentflagR=0
    
    NormL=NormR=0
    StereoNormalised=0
    PkNormVal=np.power(10,PkDb/20) #convert dB input value           
    ChL = AudioIn[:,0] #left channel of input audio   
    ChR = AudioIn[:,1] #right channel of input audio
    
    #maximum absosute value of audio file amplitude
    maxL=np.max(np.abs(ChL)) 
    maxR=np.max(np.abs(ChR)) 
    
    #Find channel with highest amplitude. 
    
    # if (maxL==maxR) and maxL==0:
    #     #Detection of silent stereo tracks L and R. Will ouput input track as dummy.
    #     silentflag=1
    #     return(AudioIn,fs,silentflag)
    silentflagL = np.all((ChL == 0))
    silentflagR = np.all((ChR == 0))
    if (silentflagL==1 and silentflagR==1):
        silentflag=1

    if silentflagL==1:
    #Detection of silent stereo tracks L and R. Will ouput input track as dummy.
        return(AudioIn,fs,silentflag)
    elif maxL>maxR:
        maxCh=maxL
    elif maxR>maxL:
        maxCh=maxR
    elif maxL==maxR:
        maxCh=maxL

    #Normalization calculation

    NormL=ChL*(PkNormVal/maxCh)
    NormR=ChR*(PkNormVal/maxCh) 
    StereoNormalised=np.stack((NormL,NormR),axis=1) #create stereo array using normalised channels.
    return(StereoNormalised,fs,silentflag)


#-----------------------------------------------------------------

f_counter=0
PkDb=0.0
Channels=0


print('')
print('Program Start...\n')
print('Values ≤ 0 recomended.\n')
PkDb=input('Enter normalisation value : ')
print('You entered:' +PkDb + ' dBFS')
PkDb=float(PkDb)
print('Choose the location of your .wav files...')

current_directory = str(SelectDir()) 
os.chdir(current_directory) #change directory to user selected directory
current_directory = os.getcwd()
file_list = []
start_time = time.time()

for file in os.listdir(current_directory):
    if file.endswith(".wav"):
        if file.startswith("._"): #to exclude ghost files starting with "._"         
            continue
        else:
            file_list.append(file) 

print('Now normalising...\n')

ListSz=float(np.size(file_list)) #Shows number of filenames contained in 'file_list' list.

if not os.path.exists("OUTPUT"): #Checks for 'OUTPUT' directory. Will make one if none there.
    os.makedirs("OUTPUT")
    
logfile=os.path.join('OUTPUT','LOG_Peak_Normalised_Wavs.txt')

f= open(logfile,"w+") #this will create a new text file, and open it.
f.write("=======[Proccessing Info]=======\n"+"\n")
f.write("Normalisation Value: "+str(PkDb)+" dBFS\n"+"\n")

for x in range(0,np.size(file_list)): #Step through file names. Read Stereo .wav files using soundfile read() function.
    
    AudioFile={}
    SilentCheck=0
    [Wav,fs]=sf.read(file_list[x])
    ChCount=ChannelCount(Wav)

    f_counter=f_counter+1
    

    if ChCount == 1:
        [Wav, SampleRate,SilentCheck]=MonoNorm(file_list[x],PkDb)
    elif ChCount == 2:
        [Wav, SampleRate,SilentCheck]=StereoNorm(file_list[x],PkDb)      
    elif ChCount>2:
        f_counter=f_counter-1
        f.write("ERROR: "+file_list[x]+" not normalised! Only Mono and Stereo files supported.\n")
        
    
    filenameNorm=os.path.join('OUTPUT', str(f_counter).zfill(3)+'.NORM_'+file_list[x]) 
    filenameShort=str(f_counter).zfill(3)+'.NORM_'+file_list[x]
    
    if ChCount<=2:
        sf.write(filenameNorm,Wav,SampleRate)
    
    if SilentCheck==0 and ChCount<=2:
        f.write("File OK: "+filenameShort+"\n")
    elif SilentCheck==1:
        f.write("WARNING: "+filenameShort+" is silent. Check original file.\n")
    

elapsed_time = time.time() - start_time
elapsed_time = round(elapsed_time, 2) 

file_str="file"

if f_counter>1:
    file_str="files"
    
f.write("\n"+"------------[Summary]----------\n"+"\n")
f.write("Processing Time: " + str(elapsed_time) + " Sec."+"["+str((elapsed_time)/60)+" Mins"+"]\n")

f.write(str(f_counter)+" normalised .wav "+file_str+" created.")
f.close()

print('Done!\n')
print(  '------------[Summary]----------\n')
print('Total Processing Time: ' + str(elapsed_time) + ' Sec.' +'['+str((elapsed_time)/60)+' Mins.]') 
print(str(f_counter)+" normalised "+file_str+" created.")
print('See LOG_Peak_Normalised_Wavs.txt in OUTPUT directory for summary.')

