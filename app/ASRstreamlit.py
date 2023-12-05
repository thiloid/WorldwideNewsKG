import streamlit as st
import rdflib
#env = shinyapplications_py
#streamlit run ASRstreamlit.py  
#
def add_logo():
    st.markdown(
        """
        <style>
            
            [data-testid="stSidebarNav"]::before {
                content: "Uni Mannheim ASR Team Project";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 20px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
                       
g=rdflib.Graph ()
g.parse('app/export_dbpedia.ttl')
print("______________________________________________________")
print("KG loaded")
print("______________________________________________________")

def optionselecter2(option):
    knows_query1 = """
    select DISTINCT ?b
    where {?x ns2:"""+ option +"""  ?b .


    }
    """

    qres1 = g.query(knows_query1)
    l=["Nothing selected"]
    for row in qres1:
        initial_value= str(row.b)
        trans_value= "\""+initial_value+"\""
        l.append(str(trans_value))
    return l

def optionselecter4(option):
    knows_query1 = """
    select DISTINCT ?b
    where {?x ns3:"""+ option +"""  ?b .


    }
    """

    qres1 = g.query(knows_query1)
    l=["Nothing selected"]
    for row in qres1:
        initial_value= str(row.b)
        trans_value= "\""+initial_value+"\""
        l.append(str(trans_value))
    return l

def optionselecter5(option, option4):
    knows_query1 = """
    select DISTINCT ?b
    where {?x ns2:"""+ option +"""  ?b .
    ?x ns5:locationCountry ?c.
    ?c ns3:country """+ option4 +""" .


    }
    """

    qres1 = g.query(knows_query1)
    l=["Nothing selected"]
    for row in qres1:
        initial_value= str(row.b)
        trans_value= "\""+initial_value+"\""
        l.append(str(trans_value))
    return l

def optionselecter(option):
    knows_query1 = """
    select DISTINCT ?b
    where {?x ns2:"""+ option +"""  ?b . 
    }
    """
    print("______________________________________________________")
    print(knows_query1)
    print("______________________________________________________")   
    qres1 = g.query(knows_query1)
    l=[]
    for row in qres1:
        initial_value= str(row.b)
        trans_value= "\""+initial_value+"\""
        l.append(str(trans_value))
    sorted_list = sorted(l)
    print("______________________________________________________")
 
    print(sorted_list)
    sorted_list.insert(0, "Nothing selected")
    return sorted_list

def query_runner(option, option2, option3):
    s= {option, option2,option3}
    var=False
    for a in s: 
        if a == "Nothing selected":
            var=True
    print("______________________________________________________")
    print(s)
    print(len(s))
    print("______________________________________________________")

    if len(s)==1 and var==True:
        return (["Nothing selected"])
    else:
       
        if option!="Nothing selected":
            add1 = "?x ns2:ActorName "+option+". ?e ns2:ActorCode ?x."
        else: 
            add1=""
        
        if option2!="Nothing selected":
             add2 = "?e ns2:Sentiment "+option2+ "."
        else: 
            add2=""

        if option3!="Nothing selected":
             add3 = "?e ns2:GoldsteinScale_Labels "+option3+ "."
        else: 
            add3=""

        knows_query = """
        select *
        where {"""+add1+ add2+ add3+""" 
        ?e ns2:SOURCEURL ?b .
        }
        """
        print("______________________________________________________")
        print(knows_query)
        print("______________________________________________________")
 
        qres = g.query(knows_query)
        l1=[]
        for row in qres:
            initial_value= str(row.b)
            l1.append(str(initial_value))
        print("______________________________________________________")
        print(l1)
        b=0
        if len(l1)==0:
            b=1
            if option!="Nothing selected":
                add1 = "?x ns2:ActorName "+option+". ?e ns2:ActorCode ?x."
            else: 
                add1=""
        
            if option2!="Nothing selected":
                add2 = "OPTIONAL{?e ns2:Sentiment "+option2+".}"
            else: 
                add2=""
            if option3!="Nothing selected":
                add3 = "OPTIONAL{?e ns2:GoldsteinScale_Labels "+option3+".}"
            else: 
                add3=""

            knows_query = """
        select *
        where {"""+add1+ add2+ add3+""" 
        ?e ns2:SOURCEURL ?b .
        }
        """
            print("______________________________________________________")
            print(knows_query)
            print("______________________________________________________")

            qres = g.query(knows_query)
            l1=[]
            for row in qres:
                initial_value= str(row.b)
                l1.append(str(initial_value))
        return l1, b

add_logo()
st.image("app/Logo.png", width=300)
st.write("""
# Wordwide News 1.0
#### To find news you never knew you wanted to read
*A knowledge graph solution*
""")

option4 = st.selectbox(
'Select an Actor Country',
(optionselecter4("country")))
st.write('You selected:', option4)

if option4!="Nothing selected":

    option = st.selectbox(
    'Who should be the an actor in the news that interests you?',
    (optionselecter5("ActorName",option4)))
    st.write('You selected:', option)
else:
    option = st.selectbox(
    'Who should be the an actor in the news that interests you?',
    (optionselecter("ActorName")))
    st.write('You selected:', option)


option3 = st.selectbox(
'What type of event should the news be about?',
(optionselecter("GoldsteinScale_Labels")))
st.write('You selected:', option3)

option2 = st.radio(
        'Do you want to see pessimistic, neutral or optimistic news?',
        key="visibility",
        options=optionselecter("Sentiment")
    )
st.write('You selected:', option2)
print("______________________________________________________")
print("Done")
print("______________________________________________________")
aa, b=query_runner(option, option2, option3)
bb= str(aa[0])
counter=0
if aa[0]=="Nothing selected":
    st.write("A total of 0 news fit your interests")
else:
    for list in aa:
        counter=counter+1
    st.write("A total of "+ str(counter)+" news fit your interests")
print("______________________________________________________")
print("Done with final query")
print("______________________________________________________")
if bb!= "Nothing selected":
    if b ==1:
        st.write("Results are only based on your chosen Actor!")
    st.write("Your Article:",bb )
    st.components.v1.iframe(bb, height=600, scrolling=True)
if len(aa)>1:
    st.write("other news you might like ")
    for i in range(len(aa)):
        if i==0:
            print("next one")
        else:
            st.write(aa[i])
