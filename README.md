# Ranking words by importance level

WordRank gets most important words from a document and ranks them in descending order based on the occurance count in transcript files. 

### Installation

Required packages listed in requirements.txt file

### Example

> from wordrank import WordRank
>
> wrank = WordRank(nwords=10)
> wrank.getrank('script.txt', 'transcript_1.txt', 'transcript_2.txt', 'transcript_3.txt')
[('food', 240), ('include', 31), ('use', 29), ('eat', 27), ('type', 15), ('culture', 8), ('animal', 6), ('price', 4), ('plant', 2), ('taste', 1)]
>
> wrank.wfreq[:10]
[('food', 222), ('include', 35), ('animal', 32), ('use', 29), ('culture', 23), ('price', 22), ('plant', 19), ('taste', 18), ('type', 18), ('eat', 18)]

<b>getrank :</b> function returns ranked list of <i>word, occurance_count</i> tuple. occurance_count is the count of the occurance in transcript files. 
<b>wfreq   :</b> parameter returns list of <i>word, occurance_count</i> tuple. occurance_count is the count of the occurance in script file.
The word <i>animal</i> is in 3-rd place in the wfreq, but it is in 7th place in final ranking.
