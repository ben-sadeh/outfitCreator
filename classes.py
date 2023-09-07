class Game:
  def __init__(self):
    self.compColours=[]
    self.rgbs=[]
    self.occasion=''
    
  def makeColours(self):
    rgbAvg=[]
    for i in range(3):
      rgbAvg.append((self.rgbs[0][i]+self.rgbs[1][i])//2)
    index=self.rgbs[2].index(max(self.rgbs[2]))
    for i in range(4):
      newColour=self.rgbs[2][:]
      if i==index:
        newColour[i]-=200
      elif i==3:
        newColour[(index+1)%3]+=200
        newColour[(index+2)%3]+=200
      else:
        newColour[i]+=200
      print(newColour)
      for j in range(len(newColour)):
        if newColour[j]>255:
          newColour[j]-=255
        if newColour[j]<0:
          newColour[j]+=255
      print(newColour)
      self.compColours.append(tuple(newColour))
    
