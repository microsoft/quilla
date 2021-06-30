Search.setIndex({docnames:["README","context_expressions","features","hooks","how_it_works","index","install","intro","makefile_vars","plugins","preface","quilla_pytest","source/modules","source/pytest_quilla","source/quilla","source/quilla.browser","source/quilla.common","source/quilla.reports","source/quilla.steps","usage","validation_files"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":3,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["README.md","context_expressions.md","features.md","hooks.rst","how_it_works.md","index.rst","install.md","intro.md","makefile_vars.md","plugins.md","preface.md","quilla_pytest.md","source/modules.rst","source/pytest_quilla.rst","source/quilla.rst","source/quilla.browser.rst","source/quilla.common.rst","source/quilla.reports.rst","source/quilla.steps.rst","usage.rst","validation_files.md"],objects:{"":{pytest_quilla:[13,0,0,"-"],quilla:[14,0,0,"-"]},"pytest_quilla.pytest_classes":{QuillaFile:[13,2,1,""],QuillaItem:[13,2,1,""],QuillaJsonException:[13,5,1,""],collect_file:[13,1,1,""]},"pytest_quilla.pytest_classes.QuillaFile":{collect:[13,3,1,""],config:[13,4,1,""],fspath:[13,4,1,""],name:[13,4,1,""],parent:[13,4,1,""],session:[13,4,1,""]},"pytest_quilla.pytest_classes.QuillaItem":{config:[13,4,1,""],fspath:[13,4,1,""],name:[13,4,1,""],parent:[13,4,1,""],reportinfo:[13,3,1,""],repr_failure:[13,3,1,""],runtest:[13,3,1,""],session:[13,4,1,""]},"quilla.browser":{browser_validations:[15,0,0,"-"],drivers:[15,0,0,"-"]},"quilla.browser.browser_validations":{BrowserValidations:[15,2,1,""]},"quilla.browser.browser_validations.BrowserValidations":{clean:[15,3,1,""],ctx:[15,4,1,""],driver_selector:[15,4,1,""],init:[15,3,1,""],run_steps:[15,3,1,""],target:[15,6,1,""],validate:[15,3,1,""]},"quilla.browser.drivers":{ChromeBrowser:[15,2,1,""],EdgeBrowser:[15,2,1,""],FirefoxBrowser:[15,2,1,""]},"quilla.common":{enums:[16,0,0,"-"],exceptions:[16,0,0,"-"],utils:[16,0,0,"-"]},"quilla.common.enums":{BrowserTargets:[16,2,1,""],OutputSources:[16,2,1,""],ReportType:[16,2,1,""],UITestActions:[16,2,1,""],URLValidationStates:[16,2,1,""],ValidationStates:[16,2,1,""],ValidationTypes:[16,2,1,""],XPathValidationStates:[16,2,1,""]},"quilla.common.enums.BrowserTargets":{CHROME:[16,4,1,""],EDGE:[16,4,1,""],FIREFOX:[16,4,1,""]},"quilla.common.enums.OutputSources":{LITERAL:[16,4,1,""],XPATH_PROPERTY:[16,4,1,""],XPATH_TEXT:[16,4,1,""]},"quilla.common.enums.ReportType":{STEP_FAILURE:[16,4,1,""],VALIDATION:[16,4,1,""]},"quilla.common.enums.UITestActions":{ADD_COOKIES:[16,4,1,""],CLEAR:[16,4,1,""],CLEAR_COOKIES:[16,4,1,""],CLICK:[16,4,1,""],HOVER:[16,4,1,""],NAVIGATE_BACK:[16,4,1,""],NAVIGATE_FORWARD:[16,4,1,""],NAVIGATE_TO:[16,4,1,""],OUTPUT_VALUE:[16,4,1,""],REFRESH:[16,4,1,""],REMOVE_COOKIE:[16,4,1,""],SEND_KEYS:[16,4,1,""],SET_BROWSER_SIZE:[16,4,1,""],SET_COOKIES:[16,4,1,""],VALIDATE:[16,4,1,""],WAIT_FOR_EXISTENCE:[16,4,1,""],WAIT_FOR_VISIBILITY:[16,4,1,""]},"quilla.common.enums.URLValidationStates":{CONTAINS:[16,4,1,""],EQUALS:[16,4,1,""],MATCHES:[16,4,1,""],NOT_CONTAINS:[16,4,1,""],NOT_EQUALS:[16,4,1,""],NOT_MATCHES:[16,4,1,""]},"quilla.common.enums.ValidationTypes":{URL:[16,4,1,""],XPATH:[16,4,1,""]},"quilla.common.enums.XPathValidationStates":{ATTRIBUTE_HAS_VALUE:[16,4,1,""],EXISTS:[16,4,1,""],HAS_ATTRIBUTE:[16,4,1,""],HAS_PROPERTY:[16,4,1,""],NOT_ATTRIBUTE_HAS_VALUE:[16,4,1,""],NOT_EXISTS:[16,4,1,""],NOT_HAS_ATTRIBUTE:[16,4,1,""],NOT_HAS_PROPERTY:[16,4,1,""],NOT_PROPERTY_HAS_VALUE:[16,4,1,""],NOT_TEXT_MATCHES:[16,4,1,""],NOT_VISIBLE:[16,4,1,""],PROPERTY_HAS_VALUE:[16,4,1,""],TEXT_MATCHES:[16,4,1,""],VISIBLE:[16,4,1,""]},"quilla.common.exceptions":{EnumValueNotFoundException:[16,5,1,""],FailedStepException:[16,5,1,""],InvalidBrowserStateException:[16,5,1,""],InvalidContextExpressionException:[16,5,1,""],InvalidOutputName:[16,5,1,""],NoDriverException:[16,5,1,""],UIValidationException:[16,5,1,""]},"quilla.common.utils":{DriverHolder:[16,2,1,""],EnumResolver:[16,2,1,""]},"quilla.common.utils.DriverHolder":{driver:[16,6,1,""]},"quilla.ctx":{Context:[14,2,1,""],get_default_context:[14,1,1,""]},"quilla.ctx.Context":{close_browser:[14,4,1,""],create_output:[14,3,1,""],default_context:[14,4,1,""],drivers_path:[14,6,1,""],is_debug:[14,6,1,""],is_file:[14,4,1,""],json_data:[14,4,1,""],load_definitions:[14,3,1,""],no_sandbox:[14,4,1,""],perform_replacements:[14,3,1,""],pm:[14,4,1,""],pretty:[14,4,1,""],pretty_print_indent:[14,4,1,""],run_headless:[14,4,1,""],suppress_exceptions:[14,4,1,""]},"quilla.hookspecs":{quilla_addopts:[14,1,1,""],quilla_configure:[14,1,1,""],quilla_context_obj:[14,1,1,""],quilla_postvalidate:[14,1,1,""],quilla_prevalidate:[14,1,1,""],quilla_resolve_enum_from_name:[14,1,1,""],quilla_step_factory_selector:[14,1,1,""]},"quilla.plugins":{get_plugin_manager:[14,1,1,""]},"quilla.reports":{base_report:[17,0,0,"-"],report_summary:[17,0,0,"-"],step_failure_report:[17,0,0,"-"],validation_report:[17,0,0,"-"]},"quilla.reports.base_report":{BaseReport:[17,2,1,""]},"quilla.reports.base_report.BaseReport":{from_dict:[17,3,1,""],from_file:[17,3,1,""],from_json:[17,3,1,""],to_dict:[17,3,1,""],to_json:[17,3,1,""]},"quilla.reports.report_summary":{ReportSummary:[17,2,1,""]},"quilla.reports.report_summary.ReportSummary":{FilterTypes:[17,2,1,""],critical_failures:[17,4,1,""],fails:[17,4,1,""],filter_by:[17,4,1,""],from_dict:[17,3,1,""],from_json:[17,3,1,""],reports:[17,4,1,""],selector:[17,4,1,""],successes:[17,4,1,""],to_dict:[17,3,1,""],to_json:[17,3,1,""]},"quilla.reports.report_summary.ReportSummary.FilterTypes":{browser:[17,3,1,""],critical_failure:[17,3,1,""],failure:[17,3,1,""],state:[17,3,1,""],successful:[17,3,1,""],target:[17,3,1,""],type:[17,3,1,""]},"quilla.reports.step_failure_report":{StepFailureReport:[17,2,1,""]},"quilla.reports.step_failure_report.StepFailureReport":{from_dict:[17,3,1,""],index:[17,4,1,""],to_dict:[17,3,1,""]},"quilla.reports.validation_report":{ValidationReport:[17,2,1,""]},"quilla.reports.validation_report.ValidationReport":{from_dict:[17,3,1,""],msg:[17,4,1,""],state:[17,4,1,""],success:[17,4,1,""],target:[17,4,1,""],to_dict:[17,3,1,""],validation_type:[17,4,1,""]},"quilla.steps":{base_steps:[18,0,0,"-"],steps:[18,0,0,"-"],validations:[18,0,0,"-"]},"quilla.steps.base_steps":{BaseStep:[18,2,1,""],BaseStepFactory:[18,2,1,""],BaseValidation:[18,2,1,""]},"quilla.steps.base_steps.BaseStep":{action:[18,4,1,""],copy:[18,3,1,""],ctx:[18,4,1,""],element:[18,6,1,""],locator:[18,6,1,""],parameters:[18,6,1,""],perform:[18,3,1,""],target:[18,6,1,""]},"quilla.steps.base_steps.BaseStepFactory":{from_dict:[18,3,1,""]},"quilla.steps.base_steps.BaseValidation":{copy:[18,3,1,""],perform:[18,3,1,""]},"quilla.steps.steps":{TestStep:[18,2,1,""]},"quilla.steps.steps.TestStep":{copy:[18,3,1,""],from_dict:[18,3,1,""],optional_params:[18,4,1,""],perform:[18,3,1,""],required_params:[18,4,1,""],selector:[18,4,1,""]},"quilla.steps.validations":{URLValidation:[18,2,1,""],Validation:[18,2,1,""],XPathValidation:[18,2,1,""]},"quilla.steps.validations.URLValidation":{perform:[18,3,1,""],url:[18,6,1,""]},"quilla.steps.validations.Validation":{from_dict:[18,3,1,""],validation_selector:[18,4,1,""]},"quilla.ui_validation":{UIValidation:[14,2,1,""]},"quilla.ui_validation.UIValidation":{browsers:[14,4,1,""],from_dict:[14,3,1,""],from_file:[14,3,1,""],from_filename:[14,3,1,""],from_json:[14,3,1,""],validate_all:[14,3,1,""],validation_type_selector:[14,4,1,""]},pytest_quilla:{pytest_addoption:[13,1,1,""],pytest_classes:[13,0,0,"-"],pytest_collect_file:[13,1,1,""],pytest_load_initial_conftests:[13,1,1,""]},quilla:{browser:[15,0,0,"-"],common:[16,0,0,"-"],ctx:[14,0,0,"-"],execute:[14,1,1,""],hookspecs:[14,0,0,"-"],make_parser:[14,1,1,""],plugins:[14,0,0,"-"],reports:[17,0,0,"-"],run:[14,1,1,""],setup_context:[14,1,1,""],steps:[18,0,0,"-"],ui_validation:[14,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","exception","Python exception"],"6":["py","property","Python property"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute","5":"py:exception","6":"py:property"},terms:{"0":[4,9,20],"06":20,"1":[4,9,14],"10":20,"16":20,"2021":20,"24":20,"3":[6,20],"4":14,"7":6,"8":6,"abstract":[17,18],"boolean":11,"case":[2,3,7,14,18,20],"class":[4,13,14,15,16,17,18,20],"default":[0,3,4,6,8,9,11,14,17,19,20],"do":[1,2,9,11,20],"enum":[3,4,12,14,15,17,18],"final":[4,9,10],"function":[2,4,9,10,11,14,15,18],"import":[9,10,14],"int":[14,17],"new":[1,2,3,4,9,10,11,14,17,20],"return":[2,3,4,9,13,14,15,16,17,18],"static":[2,10,11],"true":[2,6,11,14],"var":[0,6],"while":[1,9,15,16],A:[0,3,4,6,11,13,14,15,16,17,18,19,20],And:9,As:[1,4,9,10],At:1,By:[1,11],For:[0,1,2,3,4,8,9,10,11,14,17],If:[1,4,8,9,10,14,18],In:[0,5,7,9],It:[1,3,4,7,11,14,17],No:9,One:20,The:[0,1,3,4,6,8,9,10,11,13,14,15,16,17,18,19,20],Their:9,Then:10,There:11,These:[6,11,16],To:[0,11],Will:[14,18],With:2,__init__:9,_build:[0,8],_dist:8,_pytest:13,abil:9,abl:[1,4,9,14,20],abort:20,about:[2,11],abov:[0,9],accept:1,access:[1,9,10],accord:[4,20],act:[2,9],action:[1,3,4,5,7,9,14,16,17],action_dict:18,action_typ:18,actual:[4,9,16,17,18],ad:[1,3,4,5,7,14,17],adapt:1,add:[2,3,4,9,11,13,14,18,19],add_argu:9,add_cooki:16,addcooki:16,addit:[1,3,8,11,14],advanc:[1,11],advantag:2,after:[3,4,14],against:[14,18],aggreg:[4,14,15,18],agil:7,all:[0,1,2,3,4,6,8,9,10,11,14,15,16,18,20],allow:[1,2,3,4,7,9,11,14,15,16,18,20],almost:4,along:4,alongsid:[2,4],alreadi:[2,11,14],also:[0,1,2,6,7,9,11,18,20],alter:4,altern:[6,16],although:20,amount:1,an:[1,2,3,4,7,9,10,11,13,14,15,16,17,18,20],ani:[1,4,6,8,9,11,14,15,16,17,18,20],anoth:9,anyon:9,anywher:[1,16],api:[5,14],applic:[1,2,3,14,15,16,17,18,20],appropri:[1,4,9,14,15,16,17,18],apt:0,ar:[0,1,2,3,4,6,8,9,10,11,14,16,17,18,19,20],arbitrari:11,arg:[3,9,14],argpars:[3,14],argument:[3,5,14,18],argumentpars:[3,14],argv:14,artifact:8,aspect:10,associ:[1,4,14,16],assort:16,assum:20,assur:2,attach:[14,16],attempt:[1,3,4,14,16,17,20],attribut:20,attribute_has_valu:16,attributehasvalu:[16,20],auto:[7,8,10],automat:[5,9],avail:[0,6,9,10,11],back:20,base:[4,7,13,14,15,16,17,18,20],base_report:[12,14],base_step:[12,14],basereport:[15,17,18],basestep:18,basestepfactori:[3,14,18],basevalid:18,basic:[9,10,11],bdist_opt:8,bdist_wheel:8,becaus:1,been:[3,4,10,14],befor:[3,14,18],behaviour:[1,4,9,11,15,16,18],being:[1,3,7,14,16,18,20],belong:11,below:[1,9,11,20],benefici:[3,14],benefit:[1,2,11],better:[1,16],between:[1,9],beyond:1,binari:8,bind:[4,18],bing:[5,9],bit:16,blank:4,block:20,bool:[14,17],both:[9,11],bound:[16,18],box:9,browser:[4,9,11,12,14,16,17,18,19,20],browser_nam:17,browser_valid:[12,14],browsernam:9,browsertarget:[4,14,15,16],browservalid:[4,15],brush:10,btn:20,build:[2,5,10],built:7,bundl:[2,6,11],button:1,ca:9,call:[1,3,4,9,10,13,14,16,17],callabl:18,can:[0,1,2,3,4,7,9,11,13,14,18,20],cannot:[1,3,9,14,16],captur:[3,14],care:11,cartesian:14,caus:[4,6,16,17,20],cd:[2,7],certain:18,cfg:11,chain:[11,14,16],chang:[1,3,4,5,9,14,16],check:[0,1,2,4,6,7,10,11,16],checkout:10,chrome:[14,15,16,19,20],chromebrows:15,ci:[2,7],classic:20,classmethod:[14,17,18],clean:[8,15],clean_cmd:8,cleanup:[14,15],clear:[16,20],clear_cooki:16,clearcooki:16,cli:[0,1,3,4,5,14],cli_config:9,click:[1,16,20],clone:6,close:[4,14,15],close_brows:14,code:[1,5,7,9,10,11,14,16,18],codebas:9,collect:[2,3,13,14],collect_fil:13,collector:13,com:[1,20],come:[6,7,20],command:[0,5,6,8,10,11,14],commit:1,common:[0,12,14,15,17,18],commun:[2,9,11],compat:11,compil:1,complet:11,complex:[3,14],compon:1,concept:10,concern:11,concurr:2,conda:6,config:[1,13],configur:[2,4,5,6,7,8,10,11,13,14,15],conflict:[1,14],connect:[9,18],consid:9,consol:14,constitut:17,consum:[2,9],contain:[1,4,7,9,14,16,17,18,19,20],content:4,context:[3,4,5,10,11,13,14,15,16,17,18,19],context_data:14,context_object_nam:1,continu:[4,20],contribut:10,control:[1,3,9,14],convert:[4,14,17,18],copi:[4,14,18],correct:[1,6,18],could:[1,9,14,20],coupl:10,cover:[10,11],crash:14,creat:[0,1,4,6,9,11,13,14,15,18,20],create_output:14,creation:[4,5,18],creator:10,critic:[4,17,20],critical_failur:[9,17],ctx:[3,5,9,12,15,18],cumbersom:9,current:[4,6,9,16,18,20],cursor:20,custom:[0,2,3,5,10,11,13,14,16],d:[1,9,19,20],data:[1,3,9,10,13,14,17,18,20],date:2,deal:14,debug:[4,9,14,17,19],decid:10,declar:[5,14,17,20],decoupl:9,deep:1,def:9,default_context:14,defin:[1,2,6,14,15,16,18,20],definit:[3,4,5,10,11,14,18,19,20],definitions_dict:14,dep:[6,8],depend:[5,6,10,14],depth:1,describ:[0,1,4,9,14,17,18,19,20],descript:[1,20],design:[6,11,18],desir:[15,17,18],detail:20,detect:[0,8,10],determin:[1,4,11,14],develop:[1,10],dict:[3,14,15,17,18],dictionari:[1,3,4,14,17,18],did:2,differ:[4,9,11,14,17,18],dir:[8,9,19],directli:[1,14],directori:[4,5,9,11,14,19],disabl:[6,11],discov:[4,7,9,11],discoveri:[2,5],discuss:[9,11],displai:[2,20],dist:8,dist_dir:8,distribut:[5,6,11],div:[1,20],doc:[5,6,7,10],doc_target:[0,8],docker:19,docs_build_dir:[0,8],docstr:0,document:[2,9,10,11,14,17,19],doe:[1,5,6,9,11,14,17,20],don:[9,16],done:[4,9],doocument:0,dot:[1,3,14],download:[6,9],driver:[4,9,12,14,16,18,19],driver_selector:15,driverhold:[14,16,18],drivers_path:[9,14,19],duplic:1,dynam:[1,4,5,9,20],e:[1,3,4,10,11,14,17],each:[1,2,4,11,14,18,20],early_config:13,easi:[1,2,11],easier:[1,7],easili:[2,11],edg:[1,2,14,15,16,19,20],edgebrows:15,edit:[14,18],effect:14,egg:1,either:[3,4,14,17,20],element:[1,18,20],els:[1,9,16],enabl:[1,7,9,10,11,13,14,19],encompass:16,encount:1,encourag:11,end:[0,4,13],enhanc:[2,11],ensur:[1,14,15,20],entcard:20,entir:[4,9,11,14],entri:18,entry_point:9,entrypoint:[4,6,9,14],enumer:1,enumresolv:[14,16,17,18],enumvaluenotfoundexcept:16,environ:[0,2,4,5,6,7,8,9,10,20],epub:5,equal:[16,20],error:[1,6,20],essenti:18,etc:[0,1,3,4,8,11,14],eval:1,evalu:1,even:[0,9,11],everi:[4,6,10,20],exactli:[1,9,20],exampl:[0,1,3,5,10,11,14,17],examplesvc:14,except:[4,12,13,14,15,17,20],excinfo:13,execut:[2,3,5,8,11,13,14,15,18,20],exhaust:1,exist:[1,2,3,4,11,14,16,20],exit:[4,9,14,19],expand:1,expect:[1,18],experi:[2,14],explan:6,expos:[4,6,9,10],express:[3,5,10,14,16,18,20],extend:[1,2,9,10,11],extens:[0,9,10],extern:[1,9,14],extra:[2,18],extract:[1,14,18],f:[1,9,19],factori:[3,4,14,18],fail:[1,5,13,14,16,17,20],failedstepexcept:16,failur:[1,4,9,11,17,20],fairli:18,fals:[4,9,14,19],familiar:[2,10],far:9,favour:1,featur:11,field:[3,11,14,20],file:[0,1,3,4,5,6,7,8,9,10,13,14,17,19],filenam:[1,4,9,19],filesystem:13,filter:17,filter_bi:17,filtertyp:17,find:[9,18],find_packag:9,fine:[3,14],finish:[4,14,20],firefox:[9,15,16,20],firefoxbrows:15,first:[1,2,4,9,10],fit:[4,16],flag:[2,4,9,11,14,19],flex:20,flow:5,fly:11,focu:[2,7],focus:4,follow:[0,4,8,9,11,20],foremost:9,form:20,form_submit:1,forward:20,found:[3,9,11,14,16],fp:[14,17],framework:[7,9,11],from:[1,2,3,4,5,9,10,11,13,14,18,20],from_dict:[14,17,18],from_fil:[14,17],from_filenam:14,from_json:[14,17],fspath:13,full:[0,3,11,14],fulli:[4,11],further:[0,2,4,9,14,17],gave:14,gener:[0,3,4,10,14,15,18,20],get:[1,10,14],get_default_context:14,get_plugin_manag:14,github:5,github_example_user_password:20,give:[2,3,9,10,14,17],given:[3,9,11,14,16,17,18,19],glanc:1,global:9,go:6,goal:4,good:[10,17],googl:0,grain:[3,14],granular:9,great:11,greatli:11,group:1,h:[9,19],ha:[1,2,3,4,6,10,11,14,20],ham:1,handi:20,handl:[0,9],handler:[3,14],happen:[4,11,14],hardcod:20,has_attribut:16,has_properti:16,hasattribut:[16,20],hasproperti:[16,20],have:[1,2,3,4,7,8,9,10,11,14,15,16,17,18,19,20],header:[1,20],headersect:1,headless:[9,14],height:20,help:[0,8,9,19],here:[0,2,9,10],hint:0,hold:[1,14,18],homepag:[1,20],homepagesearchtest:1,hook:[2,4,5,9,10,14],hookspec:[2,3,5,9,12],hope:20,hover:[16,20],how:[1,2,5,6,7,10,11],howev:[4,6,9,11,20],href:20,html:[0,5],http:[1,9,20],i:[1,3,4,10,11,14,17],id:[1,14,20],identifi:1,ign:20,ignor:14,ii:20,immedi:[2,3,14],implement:[3,14],imposs:20,includ:[1,6,9,10,18],inconsist:4,incorpor:1,incred:11,inde:11,independ:[14,18],index:17,indic:[3,14,20],individu:[9,10,11,14,18],info:8,inform:[0,1,4,7,9,10],inherit:11,ini:[11,13],init:15,initi:[3,4,14,15],inject:9,inlin:1,inner:[17,18,20],input:[1,20],insid:[1,9],instal:[0,2,5,10,11],instanc:[3,4,13,14,15,18],instanti:14,instead:[9,20],instruct:[10,14],integr:[0,7,10,11,20],interact:[2,10],interfac:[5,11],intern:[14,16],invalid:16,invalidbrowserstateexcept:16,invalidcontextexpressionexcept:16,invalidoutputnam:16,inventori:11,is_debug:14,is_fil:14,isol:[2,11,13],issu:6,item:[13,20],iter:1,its:[3,4,6,11,14,16],itself:[1,4,17],json:[1,3,4,5,9,11,13,14,17,18,19,20],json_data:14,just:[1,2,3,4,6,9,14],keep:[9,11,18],kei:[4,10,11,18,20],kept:11,keystor:1,kind:[17,20],label:[11,20],last:[1,20],later:[2,9,20],latex:0,latexpdf:[0,5],leav:14,legibl:[1,4],len:9,length:9,let:[2,11],level:11,leverag:11,librari:7,like:[1,9,11,14,17],limit:[1,11],line:[0,5,9,11,14],list:[0,4,14,15,17,20],lite:20,liter:[9,16,20],littl:2,ll:[2,9],load:[1,4,9,13,14,17],load_definit:14,loader:[4,17],local:[1,2,5,7],localpath:13,locat:[14,18],log:1,logic:[3,9,11,14,18],login:[1,20],login_field:20,longer:9,look:10,macro:14,made:1,mai:[0,20],main:20,maininfocard:20,maintain:[1,7,10],make:[0,1,2,6,8,9,10,11,14],make_pars:14,makefil:[0,5,6,10],man:[0,5],manag:[4,14,15],mani:[2,11],manipul:[4,17],map:18,mark:11,markdown:0,marker:[5,7],match:[1,11,13,16,17,20],matter:9,maximum:9,mayb:9,md:20,mean:[1,4,11,18],menu:20,merg:[1,4,14],messag:[9,19],metadata:17,method:[0,6,11,15,18],might:[1,3,13,14],mind:18,minim:4,mode:[9,14,19],modifi:[3,14],modul:[0,5,9,12],more:[0,1,2,3,7,8,9,10,11,14,20],most:[1,2,3,11,14],mr:20,msedg:15,msg:17,much:16,multi:11,multipl:[1,10,11],multiprocess:11,multitud:10,must:[1,3,11,14,18],mutat:4,my:1,myservic:1,myst_pars:0,n:20,name:[0,1,3,4,8,9,11,13,14,16,17,19,20],namespac:[3,14],navig:[4,15,20],navigate_back:16,navigate_forward:16,navigate_to:16,navigateback:[16,20],navigateforward:[16,20],navigateto:[16,20],neatli:2,necessari:[14,18],necessarili:4,need:[0,2,3,8,9,10,11,14,16,18,20],never:2,newer:[1,14],next:[4,20],no_sandbox:14,node:13,nodeid:13,nodriverexcept:[16,18],non:[1,10],none:[3,9,13,14,15,16,18,19,20],normal:1,not_attribute_has_valu:16,not_contain:16,not_equ:16,not_exist:16,not_has_attribut:16,not_has_properti:16,not_match:16,not_property_has_valu:16,not_text_match:16,not_vis:16,notattributehasvalu:16,notcontain:[16,20],note:[0,6],notequ:[16,20],notexist:[16,20],nothasattribut:[16,20],nothasproperti:[16,20],notmatch:16,notpropertyhasvalu:[16,20],nottextmatch:[16,20],notvis:[16,20],now:9,number:[11,17],numer:17,object:[2,3,4,5,9,10,13,14,15,16,17,18,19],occur:[4,20],offer:11,omit:[11,14,20],onc:4,one:[1,2,9,10,14,17,20],onli:[4,5,6,9,17,18],onto:20,open:[4,14,16],oper:[1,20],oppos:11,opt:[9,11],option:[0,3,4,5,6,7,8,9,13,14,17,18],optional_param:18,order:[1,4,14],ordinarili:20,origin:[11,14],os:1,other:[1,2,4,6,9,16],otherwis:[3,4,13,14,20],our:[1,9],out:[0,2,7,9,10],output:[1,3,4,5,8,9,11,14,16,19],output_nam:14,output_valu:16,outputnam:[9,20],outputsourc:[4,16],outputvalu:[1,9,16,20],outsid:9,over:[3,9,14,20],overrid:[1,3,14],overview:5,own:[2,9,20],owner:7,p:[9,19],packag:[5,10,11,12],package_opt:8,package_target:8,page:[1,4,20],paradigm:2,parallel:11,paramet:[1,3,4,9,11,13,14,15,17,18,20],parameternam:20,parent:[13,18],pars:[3,4,14],parser:[3,4,9,13,14],part:[1,2,7,10],particularli:1,pass:[1,2,3,4,11,14,15,17],password:[1,2,20],passwordinputfield:20,path:[1,3,4,9,13,14,20],path_to_valu:1,pattern:20,pdf:0,perform:[1,4,7,13,14,17,18,20],perform_replac:14,perhap:9,permiss:14,pick:9,pip:[0,6,9],pipelin:2,place:[1,11,16],platform:9,pluggin:[3,14],plugin:[1,4,5,6,10,12],plugin_manag:14,plugin_root:14,pluginmanag:14,pm:14,popul:1,posit:[5,9,20],possibl:[3,8,9,11,14],potenti:1,pre:[2,14],precis:20,predefin:9,prefac:5,prefer:[0,6,14],prefix:[5,13],pretti:[2,9,14,19],pretty_print_ind:14,prevent:11,previou:[1,9],primari:20,print:[4,9,14,19],process:[0,4,6,9,10,11,14,20],produc:[0,2,4,9,11,14,15,17,18,20],product:14,program:[9,19],programm:9,programmat:2,project:[0,6,7,9,11],proper:[1,4,17,18],properli:11,properti:[14,15,16,18,20],property_has_valu:16,propertyhasvalu:[16,20],provid:[0,1,6,9,11,17,19,20],publish:[2,9,10],puppi:[1,5],pure:1,purpos:17,put:4,py:[0,2,4,5,9,14],pytest:[5,6,7,10],pytest_addopt:13,pytest_class:[5,12],pytest_collect_fil:13,pytest_load_initial_conftest:13,pytest_quilla:[5,12],python3:8,python:[0,1,4,5,7,8,11],python_execut:8,q:20,qa:10,quickli:1,quilla:[0,1,2,8,9,10,12,13,20],quilla_addopt:[3,4,9,14],quilla_configur:[3,4,9,14],quilla_context_obj:[3,9,14],quilla_postvalid:[3,4,14],quilla_prevalid:[3,4,14],quilla_resolve_enum_from_nam:[3,14],quilla_step_factory_selector:[3,14],quilla_step_selector:[3,14],quillafil:13,quillaitem:13,quillajsonexcept:13,quillaplugin:9,rais:[4,13,15,16,18],raw:[9,14,19],re:[10,11],react:[1,20],read:[1,4,10,11,14,17,20],realli:16,reason:11,receiv:9,recogn:16,recommend:5,recover:20,recreate_context:14,recurs:1,reduc:1,refer:[5,10,14],referenc:20,refresh:[16,20],regard:10,regardless:[11,14],regener:17,regist:[3,4,6,11,14],regular:[7,20],rel:[0,20],releas:2,relev:14,remain:[6,11],remaind:[3,14],remot:[15,16,18],remove_cooki:16,removecooki:16,repetit:1,replac:[1,14],repo:0,report:[3,4,5,9,12,14,15,16,18,19,20],report_dict:17,report_json:17,report_summari:[12,14],report_typ:17,reportinfo:13,reportsummari:[3,4,9,14,17,20],reporttyp:[16,17],repositori:[6,9,11],repr_failur:13,repres:[1,14,17,18],represent:[9,17,19],reproduc:2,request:18,requir:[0,1,3,4,6,9,11,14,16,18,20],required_param:18,requisit:18,requri:16,reset:15,resolv:[1,3,4,9,14,16,18],rest:[4,11,14],result:[1,2,4,14,17,18,20],resultspag:20,retriev:[1,3,9,13,14,16],rich:5,right:9,robust:11,root:[0,3,4,9,14,15],rtd:0,run:[0,1,4,5,6,7,8,9,10,13,14,15,18,19,20],run_headless:[9,14],run_step:15,runtest:13,runtim:[1,3,4,14,15,18],s:[2,9,11],same:[4,9,11,20],sandbox:[14,19],save:[4,14],sb_form_go:20,sb_form_q:20,scenario:4,schema:18,school:10,scope:[0,13],script:18,sdist:8,sdist_opt:8,seamlessli:[2,9],search:[1,5,9,14],searchbutton:20,searchsubmitbutton:1,searchtextbox:20,searchtextfield:1,second:1,secondli:9,secret:[1,9,10],section:[9,10,20],see:[0,1,4,9,10],seek:[10,18],seem:6,select:[4,18],selector:[3,4,14,17,18],selenium:[4,15,16,18],selenium_tool:15,self:13,send_kei:16,sendkei:[1,16,20],sensit:1,separ:[0,1,3,11,14],sequenti:4,seri:[17,20],session:[13,14],set:[1,4,6,8,9,11,14,15,18,19,20],set_browser_s:16,set_cooki:16,setbrowsers:[16,20],setcooki:16,setup:[0,3,4,9,11,14,20],setup_context:14,setup_step:14,setuptool:[6,9],sever:6,shallow:[14,18],share:[14,16,18],ship:6,should:[0,1,3,6,8,9,10,11,13,14,18],show:[9,11,19],shown:20,sign:5,signinbutton:[1,20],signinpag:20,silent:1,simpl:18,simpli:11,simplifi:11,sinc:[1,4,6,10,11,14],singl:[11,14,18,20],sitetitl:9,size:20,skip:11,skipif:11,slow:11,small:9,snapshot:4,so:[1,4,7,9,10,11,14,18],some:[3,9,11,14,16,20],someon:9,someth:[4,6],sourc:[3,4,6,8,9,10,14,16,20],space:0,spam:1,specif:[0,4,8,9,10,11,14,15,16,18,20],specifi:[0,1,3,4,11,14,15,17,18,20],speed:11,sphinx:0,sphinx_argparse_cli:0,sphinx_autodoc_typehint:0,ss:20,standard:4,start:[10,11,13,14,15,20],state:[1,3,4,9,14,15,16,17,18,20],statu:[11,14],step:[1,2,3,4,7,9,12,14,15,16,17,20],step_failur:16,step_failure_report:[12,14],step_index:17,stepfailur:16,stepfailurereport:[4,17,20],stepsaggreg:[4,15],still:[9,11,15],store:[1,3,9,10,14,15,19],store_tru:9,str:[3,13,14,15,17,18],str_valu:16,straightforward:18,string:[1,2,3,4,9,14,16,17,18,19,20],structur:[10,14],style:[5,10],subclass:[3,4,14,15,18],submit:1,submitbutton:[1,20],submodul:[5,12],subpackag:[5,12],subsect:10,substanti:4,substep:15,substr:20,success:[9,11,17,20],suit:[2,5],suitabl:14,summar:[18,20],summari:[3,14,17],summary_dict:17,summary_json:17,support:[1,5,9,14,16,17,18],suppos:9,suppress:14,suppress_except:[4,14],sure:[1,2,6,10],swap:9,sy:14,syntax:[1,2,4,6,7,16,17],system:[4,9],t:[3,9,14,16],tabl:[0,1,20],take:[2,7,11],taken:[4,17],target:[0,1,4,5,9,15,16,17,18,20],targetbrows:[1,9,20],team:10,test:[1,3,4,5,10,13,14,16,17,18,20],test_:11,test_data:13,tester:2,teststep:[4,18],tex:0,texliv:0,text:[1,14,20],text_match:16,textmatch:[16,20],than:9,thei:[0,1,3,4,6,9,10,11,14,20],them:[1,2,4,10,14,17],theme:0,themselv:[3,11,14],therefor:[0,20],thi:[0,1,3,4,6,7,8,9,10,11,13,14,16,17,18,19,20],those:[0,2,11],though:[0,6],three:18,thrive:2,through:[0,1,2,4,7,9,10,11,14,15,17,20],throughout:16,time:[1,4,9,11,20],timeoutinsecond:20,titl:9,to_dict:17,to_json:17,togeth:11,too:9,tool:11,top:11,total_report:9,tox:11,track:11,tradit:11,translat:4,treat:[9,19],trust:17,tune:14,tupl:[3,14],turn:[7,11],two:9,type:[0,1,3,4,14,15,16,17,18,20],type_:18,typo:1,ui:[1,5,9,14,16,19,20],ui_valid:[5,12],uiconf:[2,4,5,9,14],uitestact:[3,4,14,16,17,18],uivalid:[3,4,9,14,15,16,18],uivalidationexcept:16,ultim:4,unbind:4,uncaught:4,unchang:11,under:18,understand:[1,7,10],unexpect:[1,11,17],unfamiliar:10,union:[17,18],uniqu:[11,13],unless:11,unrecover:[17,20],until:[1,6,20],up:[2,4,9,10,11,14,15,18],updat:18,url:[1,5,14,15,16,18],url_root:15,urlvalid:18,urlvalidationst:[14,16,18],us:[0,1,2,3,4,5,6,7,8,9,10,14,15,16,17,18,19,20],usag:[0,5,9],usecas:11,user:[0,2,4,7,9,10,11,14,20],usermenuicon:20,usernam:20,usernameinputfield:20,usual:[11,17],util:[12,14,17,18],valid:[3,4,5,9,10,12,14,15,16,17,19],validate_al:[3,4,14],validation_dict:18,validation_json:14,validation_paramet:14,validation_report:[12,14],validation_selector:18,validation_typ:17,validation_type_selector:14,validationreport:[17,18,20],validationst:[4,14,16,18],validationtyp:[4,14,16,18],valu:[0,1,2,3,4,5,14,16,18],variabl:[0,1,2,4,5,6,9,10,14],variou:[10,11,17],venv:6,version:[5,8,9],virtual:[6,8],virtualenvwrapp:6,visibl:[16,20],visual:2,w3c:10,wa:[1,4,6,7,11,13,14,17],wai:[1,3,9,14,17,20],wait:20,wait_for_exist:16,wait_for_vis:16,waitforexist:[16,20],waitforvis:[16,20],want:[1,9,10,18],we:[1,9],web:[10,18,20],webdriv:[15,16,18],webel:18,websit:10,welcomepag:20,well:[1,2,9,17],were:[4,14],what:[0,2,3,7,9,10,14,18,20],wheel:[5,6],when:[1,3,4,5,8,10,13,14,16,20],whenev:[1,9],where:[1,3,9,13,14,19],wherev:14,whether:[9,11,14,17,19],which:[0,2,3,4,8,9,10,11,14,18,20],whl:[6,8],who:[9,10],why:5,width:20,window:4,wish:9,within:[11,13,18,20],without:[9,11,16],work:[1,5,6,10,11,14],workabl:4,worri:2,would:[1,4,7,9,17,18],wrapper:[4,18],write:[1,2,7,9,10,11,20],writer:[1,4,7,10,14],written:[10,11,20],wrong:6,www:20,xdist:[2,5],xpath:[1,5,10,14,16,18],xpath_properti:16,xpath_text:16,xpathproperti:[16,20],xpathtext:[16,20],xpathvalid:18,xpathvalidationst:[4,14,16,18],yield:13,you:[0,1,2,6,7,8,9,10,17,18,20],your:[1,2,6,7,9,10],yourprofiledropdown:20,yourself:2},titles:["Documentation","Context Expressions","Features","Quilla Plugin Hooks","How does Quilla work?","Welcome to Quilla\u2019s documentation!","Installation","Quilla","Makefile Variables","Plugins","Preface","Running Quilla tests with Pytest","API Reference","pytest_quilla package","quilla package","quilla.browser package","quilla.common package","quilla.reports package","quilla.steps package","Command-Line Usage","Validation Files"],titleterms:{"enum":16,"new":18,In:20,action:[18,20],ad:[9,11,18],api:12,argument:[9,19],automat:11,base_report:17,base_step:18,bing:20,browser:15,browser_valid:15,build:[0,6,8],chang:[8,11],cli:[9,11,19],code:[4,6],command:19,common:16,configur:9,content:5,context:[1,2,9],creation:11,ctx:14,custom:6,declar:[2,7],definit:1,depend:0,directori:[0,8],discoveri:[9,11],distribut:8,doc:[0,8],document:[0,5],doe:4,driver:15,dynam:[2,11],environ:1,epub:8,exampl:[8,9,20],except:16,execut:4,express:[1,2,9],extens:2,fail:11,featur:2,file:[2,11,20],flow:4,from:0,github:20,hook:3,hookspec:14,how:4,html:8,instal:[6,9],integr:2,interfac:19,json:[2,7],latexpdf:8,line:19,local:9,makefil:8,man:8,marker:11,modul:[13,14,15,16,17,18],object:1,onli:[8,11],option:[11,19],output:[2,20],overview:1,packag:[0,6,8,9,13,14,15,16,17,18],plugin:[2,3,9,11,14],posit:19,prefac:10,prefix:11,puppi:20,py:11,pytest:[2,11],pytest_class:13,pytest_quilla:13,python:6,quilla:[3,4,5,6,7,11,14,15,16,17,18,19],recommend:6,refer:12,report:[2,11,17],report_summari:17,rich:11,run:11,s:5,search:20,sign:20,step:18,step_failure_report:17,style:0,submodul:[13,14,15,16,17,18],subpackag:14,suit:11,support:[11,20],system:2,target:8,test:[2,7,11],ui:[2,7],ui_valid:14,uiconf:11,url:20,us:11,usag:19,util:16,valid:[1,2,18,20],validation_report:17,valu:20,variabl:8,version:6,welcom:5,wheel:8,when:11,why:[9,11],work:4,xdist:11,xpath:20}})