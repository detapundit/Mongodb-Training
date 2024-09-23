        mongostat -o='host,opcounters.insert.rate()=Insert Rate,opcounters.query.rate()=Query Rate,opcounters.command.rate()=Command Rate' 
        --rowcount=3 "mongodb+srv://dbaTestAdmin@m0cluster-restored.iy0a1o4.mongodb.net" 2
    
    
        mongostat --discover --humanReadable=true mongodb+srv://hawaii-dba-labs-user:nNVAWqNmiz22GV7J@instruqttest.3xfvk.mongodb.net 3
    
    
        mongotop “mongodb+srv://dbaTestAdmin@cluster0.mntqoh9.mongodb.net” 2 --rowcount=3
        mongotop 30 --uri='mongodb+srv://username@businesscluster.iy0a1o4.mongodb.net'
        mongotop mongodb+srv://hawaii-dba-labs-user:nNVAWqNmiz22GV7J@instruqttest.3xfvk.mongodb.net 3
    
    
        bsondump --pretty accounts.bson
        bsondump --outFile=grades.json -–pretty grades.bson
