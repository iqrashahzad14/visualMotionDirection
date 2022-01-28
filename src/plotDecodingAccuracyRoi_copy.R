rm(list=ls()) #clean console


library(ggplot2)
library(doBy)
library(cowplot)
library(Rmisc)
library(stringr)

library(dplyr)
library(tidyverse)

#######################################################
pathResults <- '/Users/battal/Dropbox/Work/CPPLab/Cerens_files_old/Result_sheets/'

########

mvpa <- NA

#dataNames <- paste(pathCosmoResults, '*.csv', sep ='/')
dataNames = "*20210524.csv"
temp = list.files(path = pathResults,pattern=dataNames)
csvFileNb <- length(temp)     

resultFiles = list()
for (i in 1:csvFileNb) {
  fileToRead = paste(pathResults, temp[i], sep ='/')
  x  = read.csv(fileToRead)
  x$FileID <- i
  resultFiles[i] = list(x)
}

# bind txt files using rbind comment
mvpa = do.call(rbind, resultFiles)

#####
### DECODING EB - SC PT-V5
#### order things a bit for easy manipulation for plotting

#make sure subjects are factor
mvpa$sub <-as.factor(mvpa$sub)

#make group order to call them in plot EB first
mvpa$group_order<-ifelse(mvpa$group == 'EB', 1, 2)
mvpa$group <-ifelse(mvpa$group == 'CONT', 'SC', 'EB')

#make roi order to call accordingly
mvpa$roi_order <- ifelse(mvpa$roi == 'lV5_6mm_2.nii', 1, 
                         ifelse(mvpa$roi == 'rV5_6mm_2.nii', 2, 
                                ifelse(mvpa$roi == 'lPT_6mm_mo.nii', 3,4)))

mvpa$roiName <- ifelse(mvpa$roi == 'lV5_6mm_2.nii', 'LeftV5', 
                         ifelse(mvpa$roi == 'rV5_6mm_2.nii', 'RightV5', 
                                ifelse(mvpa$roi == 'lPT_6mm_mo.nii', 'LeftPT','RightPT')))

#add motion or static condition
mvpa$isMotion <- ifelse(tolower(substring(mvpa$conditions, 1, 1)) == 's',0,1) 
mvpa$condition <- ifelse(tolower(substring(mvpa$conditions, 1, 1)) == 's','static','motion') 

# filter out some unnecassary columns
# filter out plane column 
mvpa[,6] <- NULL
mvpa[,6] <- NULL
mvpa[,7] <- NULL
mvpa[,7] <- NULL
mvpa[,4] <- NULL

# let's multiple accuracy with 100
mvpa$value <- mvpa$value * 100
mvpa.motion <- subset(mvpa, isMotion ==1)
mvpa.static <- subset(mvpa, isMotion == 0)

# define hemisphere
mvpa$hemis <- ifelse(mvpa$roiName == 'LeftV5', 'left', 
                      ifelse(mvpa$roiName == 'RightV5', 'right', 
                             ifelse(mvpa$roiName == 'LeftPT', 'left','right')))

# redefine the within/across axis column
names(mvpa)[5]<-paste("isWithin")
mvpa.within <- subset(mvpa, isWithin == 1 | isWithin ==3)
# only choose motion to see axis of motion exist?
mvpa.within <- subset(mvpa.within, isMotion == 0)

###### see below for further anova on these #####



# take only 4 motion
mvpa.4MS <- subset(mvpa, conditions == 'Motion4' | conditions =='Static4')
# below does not work because it converts the second letter lower case, I want: SLeftvsRight
# mvpa.static$conditions <-str_to_title(mvpa.static$conditions)

# # take only 4 motion
# mvpa.4motion <-subset(mvpa.motion, conditions =='Motion4')
# mvpa.4static <-subset(mvpa.static, conditions =='Static4')


# summary stats
mvpa.4MS$condRoi <- paste(mvpa.4MS[,'condition'], mvpa.4MS[,'roiName'])

# small trial to only see one condition one roi across subjects
# mvpa.4M <- subset(mvpa.4MS, conditions == 'Motion4' & roiName == 'RightV5')
  
df <- summarySE(data = mvpa.4MS, 
                groupvars=c('group', 'group_order', 'condRoi','roiName', 'roi_order','condition'),
                measurevar='value')
df

setlimit = c(10,55) 
setbreak = c(10,20,30,40,50)

shapesize = 2
shapetype = 21
shapestroke = 1
transparent = 1 #0.6
jitter  = position_jitterdodge(0.2) # position_jitter(width=0.3)


fig <- ggplot(data = mvpa.4MS, 
              aes(x = reorder(condRoi,roi_order), 
                  y = value, 
                  color = group,
                  group = group)) +
  geom_point(data=mvpa.4MS,aes(x = reorder(condRoi,roi_order), y = value), size = shapesize,
             position = jitter, shape = shapetype, stroke = shapestroke) + 
  
  stat_summary(aes(color=group), fun=mean, fun.min = mean, fun.max = mean, geom="crossbar", size=0.6, width=0.6,position = position_dodge(width=.75)) +
  
  theme_classic() +
  geom_errorbar(data = df, 
                aes(ymin = value-se, ymax = value+se, group = reorder(group, group_order)), 
                color = 'black',size=0.5, width=0.15, alpha = transparent, position = position_dodge(width=.75)) +


  geom_hline(yintercept=c(25), linetype="dotted", colour="black", size=.5) +
  ggtitle("") +
  ylab("Decoding Accuracy (%)") +
  xlab("") +
  theme(axis.text.x=element_text(size=8, face = 'bold', angle=0, colour='black')) + # face = 'bold', 
  theme(axis.text.y=element_text(size=8, angle=0, colour='black')) +
  theme(axis.title.y=element_text(size=11, angle=90, colour='black')) +
  scale_y_continuous(limits=setlimit, breaks=setbreak, position="left") +
  scale_x_discrete(labels = c("Moving","Static","Moving","Static","Moving","Static","Moving","Static"))+
  # theme(text=element_text(family="Microsoft Sans Serif")) +
  scale_color_manual(values=c("purple","gray")) +
  theme(legend.position="none")
fig

filename <- paste(pathCosmoResults, 'Decoding_4Motion4Static_EBSC.png', sep = '')

# ggsave(filename, fig, dpi=300, width=8, height=2.4)

ggsave(filename, fig, dpi=300, width=4.5, height=3)

#### add fonts for ggpplot. 
filename <- paste(pathCosmoResults, 'Decoding_4Motion4Static_EBSC.pdf', sep = '')
ggsave(filename, fig, dpi=300, width=8, height=2.4)


###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### 
###### within vs. across motion decoding #####
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### 

# rename the rois etc for anova options
mvpa.within$roi <- ifelse(mvpa.within$roiName == 'LeftV5', 'V5', 
                          ifelse(mvpa.within$roiName == 'RightV5', 'V5', 
                                 ifelse(mvpa.within$roiName == 'LeftPT', 'PT','PT')))


mvpa.within$sub <- as.factor(mvpa.within$sub)
mvpa.within$roi <- as.factor(mvpa.within$roi)
mvpa.within$group <- as.factor(mvpa.within$group)
mvpa.within$hemis <- as.factor(mvpa.within$hemis)

head(mvpa.within)

mvpa.within[,9] <- NULL
mvpa.within[,9] <- NULL

# only keep binary decodings
mvpa.within<- subset(mvpa.within, conditions != 'Motion4')
#mvpa.within<- subset(mvpa.within, conditions != 'Static4') # if we are looking at Static conditions instead of motion


#rename columns
names(mvpa.within)[7]<-'roiOrder'
names(mvpa.within)[8]<-'roiHemi'
names(mvpa.within)[6]<-'groupOrder'


# let's see some summary stats
df <- summarySE(data = mvpa.within, 
                groupvars=c('group', 'roiHemi', 'isWithin'),
                measurevar='value')
df

mvpa.within$isWithin<-as.factor(mvpa.within$isWithin)
mvpa.within$group<-as.factor(mvpa.within$group)
mvpa.within$conditions<-as.factor(mvpa.within$conditions)
mvpa.within$hemis<-as.factor(mvpa.within$hemis)
mvpa.within$roiHemi<-as.factor(mvpa.within$roiHemi)
mvpa.within$roi<-as.factor(mvpa.within$roi)


# test homogenity
mvpa.within %>%
  group_by(roiHemi, isWithin) %>%
  levene_test(value ~ group)

# # test normality - crashes 
# mvpa.within.1 <-subset(mvpa.within, isWithin ==1
#                        )
# mvpa.within.1 %>%
#   group_by(roi, hemis, conditions, group) %>%
#   shapiro_test(value)



# let's try anova' - but it is "unequal"
# why? 2 conditions for within-axis (LeftvsRight, and UpvsDown)
# 4 conditions for across-axis (LeftvsUp, LeftvsDown, RightvsUp, RightvsDown)

my.anova <- ezANOVA(data=mvpa.within, 
                    dv=.(value), 
                    wid=.(sub), 
                    within =.(isWithin, roiHemi), 
                    between=.(group), 
                    detailed=TRUE, 
                    type=3) #

my.anova


# let's try including "conditions" into model instead of isWithin
my.anova <- ezANOVA(data=mvpa.within, 
                    dv=.(value), 
                    wid=.(sub), 
                    within =.(conditions, roi, hemis), 
                    between=.(group), 
                    detailed=TRUE, 
                    type=3) #

my.anova

# let's look at the mean values to make sense of pairwise-t.test:
df <- summarySE(data = mvpa.within, 
                groupvars=c('roiOrder', 'conditions'),
                measurevar='value')
df


# look at the "conditions" pairwise ttest
# if we do not have condition difference within "within", then we can aggregate these, to have an anova with fewer levels
pairwise.t.test(mvpa.within$value, mvpa.within$conditions, pool.sd = F, p.adjust.method="bonferroni")

# now we can aggregate conditions into 2 sub-category - within and across


# to avoid such unbalance - we can average Left and Right across condition decoding
mvpa.within.1 <-subset(mvpa.within, isWithin == 1)
mvpa.within.3 <- subset(mvpa.within,isWithin ==3)

a<- mvpa.within.3
mvpa.new.across <- aggregate(a$value, FUN = mean,
                             by = list(sub = a$sub, group = a$group,isWithin = a$isWithin, 
                                       groupOrder = a$groupOrder, 
                                       roiOrder = a$roiOrder, roiHemi = a$roiHemi, hemis = a$hemis, roi = a$roi))

b<- mvpa.within.1
mvpa.new.within <- aggregate(b$value, FUN = mean,
                             by = list(sub = b$sub, group = b$group,isWithin = b$isWithin, 
                                       groupOrder = b$groupOrder, 
                                       roiOrder = b$roiOrder, roiHemi = b$roiHemi, hemis = b$hemis, roi = b$roi))

names(mvpa.new.across)[9] <- 'value'
names(mvpa.new.within)[9] <- 'value'


#combine back the datasets
withinacross <- rbind(mvpa.new.within, mvpa.new.across)

# let's look at summary stats
df <- summarySE(data = withinacross, 
                groupvars=c('roiOrder',  'roiHemi', 'group', 'isWithin'),
                measurevar='value')
df


# test homogenity
withinacross %>%
  group_by(roiHemi, isWithin) %>%
  levene_test(value ~ group)

# test normality - still crashes 
# str(withinacross)
# 
# withinacross %>%
#   group_by(group) %>%
#   shapiro_test(value)


#let's see with anova now
my.anova <- ezANOVA(data=withinacross, 
                    dv=.(value), 
                    wid=.(sub), 
                    within =.(isWithin, roi, hemis), 
                    between=.(group), 
                    detailed=TRUE, 
                    type=3) #

my.anova

##### now reorganise the data to open in JASP ####
# quick trial to move data into columnar structure for JASP
temp <- withinacross
head(temp)
temp[,4] <-NULL
temp[,4] <-NULL
temp[,5] <-NULL
temp[,5] <-NULL


aa<- subset(temp, roiHemi == 'LeftPT' & isWithin == 1)
bb<- subset(temp, roiHemi == 'RightPT' & isWithin == 1)
cc<- subset(temp, roiHemi == 'LeftV5' & isWithin == 1 )
dd<- subset(temp, roiHemi == 'RightV5' &  isWithin == 1 )


ee<- subset(temp, roiHemi == 'LeftPT' & isWithin == 3)
ff<- subset(temp, roiHemi == 'RightPT' & isWithin == 3 )
gg<- subset(temp, roiHemi == 'LeftV5' & isWithin == 3)
hh<- subset(temp, roiHemi == 'RightV5' &  isWithin == 3)


temp2 <- cbind(aa, bb$value, cc$value, dd$value, ee$value, ff$value, gg$value, hh$value)

head(temp2)
#organise a bit more
temp2[,3] <-NULL
temp2[,3] <-NULL

names(temp2)<-c('sub', 'group', 'lPT_w',  'rPT_w', 'lV5_w', 'rV5_w',
                'lPT_a', 'rPT_a', 'lV5_a', 'rV5_a')
                
# write as .csv
write.csv(temp2, 'WithinAcrossDecoding_2Condition_Static_EBSC_V5PT_12112021.csv', row.names = FALSE)

