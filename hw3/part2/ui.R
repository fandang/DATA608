require(shiny)

shinyUI(pageWithSidebar(
  headerPanel("HW 3B: Compare State to National Averages"),
  sidebarPanel(

    selectInput("CauseOfDeath", label = h3("Cause Of Death:"),  choices = list(
      "Certain infectious and parasitic diseases", 
      "Neoplasms", 
      "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism Endocrine, nutritional and metabolic diseases", 
      "Mental and behavioural disorders", 
      "Diseases of the nervous system", 
      "Diseases of the ear and mastoid process", 
      "Diseases of the circulatory system", 
      "Diseases of the respiratory system", 
      "Diseases of the digestive system", 
      "Diseases of the skin and subcutaneous tissue", 
      "Diseases of the musculoskeletal system and connective tissue", 
      "Diseases of the genitourinary system", 
      "Pregnancy, childbirth and the puerperium", 
      "Certain conditions originating in the perinatal period", 
      "Congenital malformations, deformations and chromosomal abnormalities", 
      "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified", 
      "Codes for special purposes", 
      "External causes of morbidity and mortality"), 
      selected = "Neoplasms"),
    
    selectInput("StateToCompareTo", label = h3("US State:"),  choices = list(
      "AL","AK","AZ","AR","CA","CO","CT",
      "DE","DC","FL","GA","HI","ID","IL",
      "IN","IA","KS","KY","LA","ME","MD",
      "MA","MI","MN","MS","MO","MT",
      "NE","NV","NH","NJ","NM","NY",
      "NC","ND","OH","OK","OR","PA",
      "RI","SC","SD","TN","TX","UT",
      "VT","VA","WA","WV","WI","WY"), 
      selected = "NY")
    
  ),
  mainPanel(
    h3(textOutput("statusLabel")), 
    htmlOutput("gvis")
  )
)
)