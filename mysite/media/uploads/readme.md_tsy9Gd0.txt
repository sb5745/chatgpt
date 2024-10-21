20024.3.20 DEP에 따라 currentPPE가 감소하여 다시 currentDEP가 감소하는 문제 해결
           	basePPE 사용
	public class CostNProfit : OperatingAsset
	public void Input_DEP()
   	 {	
      	  if (currentDEP == 0)  basePPE = inputPPE.currentPPE;   

       	 inputPPE.currentPPE -= float.Parse(inputField_DEP.text);
       	 // 감가상각 계산
        	currentDEP = (basePPE * 0.25f);
	}

2024.3.22 
	Dropdown 버튼 3개(FifO, 자산부채입력창 보이기, 재무상태표  Mean/Difference
	매추채권 버튼 : inputSales 창(매출, 외상매출재권) 보이기
	자산 부채 입력필드 수정 : null이더라도 0으로 간주하고 설정
4.05
	재고자산 설명방식 변경 : Production1, Production2 -> Production1 복수 클릭
	재고생산(Production1)에 Produce 스크립트 붙어 있으므로 유의
	무지개색 변화  ChangeRainbowColor()
	색상을 숫자 대신 이름으로 표시 UtilityTools.GetColorNameFromColor((Color color))
4.06 
	재고자산, FOFO, LIFO, Reset.
	치킨의 이동순서 반영, 재고자산의 변화, 매출원가의 변화 반영
4.17 활동성 게임 완성  
       회전 버튼 누르면 사이즈 조정 및 위치 이동하여 회전
       재고자산 회전율은 매출원가를 기준으로 회전
       RESET 완성, CHICKENSpRODUCED 정보 저장후  RESET시 복원에 사용
      invalueHistory외에 invalueColorHistory 생성. 
       inventoryController 에서 Add되던 invalueColorHistory를 produce.1buttonClicked메서드에서 Add
       색상과 invalue를 튜플로 저장(시도중)
       ChangeRAinbowColor 메서드가 이중 실행되지 않도록 수정(색상이 주황부터 나오는 것 수정)
4.18
      invalue와 색상이 같은 줄에 같은 색상르로 표시 invalueColorHistoryUpdate()
      이름은 첫번째부터 색상은 두번때부터 시작하는 오류 해결 .. public clickCount = -1;	
      색상을 숫자대신 색상 이름으로 표시
5.06 
	SingletonManager 완성 SingletonManager.Instance.data 및  SingletonManager.Instance.TxtData로 접근
         Capatal, IlliquidDebt, LiquidDebt, PPE, Intangible, Investment, INventory, Receivable, Cash 싱글톤 변수
	CostNProfit을 Singleton으로 완성. CostNProfit.Instance.로 접근
	CurrentSales, CurrentCGS, CurrentDEP,  CurrentSGA, CurrentINTEREST, CurrentTAX, CurrentNI 싱글톤 변수
	TXT가 두 군데서 호출되는 경우 예상치 못한 디스플레이 발생
	UpdateCostValues에서 이중 업데이트되지 않도록 주의
	
5.07
	안전성게임 버튼 누르면 게임 시작, 크기는 부채비율에 따라 변하고 부채는 왕복운동
	Shield프리팹 씬에서는 지우되 프리팹이 모든 곳에서 적절히 할당되어야 함
	ActivityGame, 게임 중딘되면 원위치 및 원래 크기로 복귀 창 내리기 중단
	
5.14
	재무상태표1 UITextManager의 폰트 자동설정 코딩이 적용이 안됨.. 
	minFont 10, maxFont20의 AutoSizeTextSetup이 할당되어 있었음. Uncheck
5.15
	UITxtManager(TxtData로 개명)의 UpdateTexts(0 내용이 사실은 CreateTexts()였음
	        SingletonManager.Instance.txtData.UpdateTexts();를 반복 클릭하면 여러번 자식패널들이 생성.
	CreateTexts()로 개명하고 Start()에서 Create 한번만 수행 
	새로 만든 UpdateTexts()는 다른 스크립트에서 수행 -- 
	CreateTexts와 UpdateTexts에서 공통으로 사용할 수 있는 객체의 참조를 Dictionary로 만듬
	Dictionary<string, TextMeshProUGUI> textReferences = new Dictionary<string, TextMeshProUGUI>();
	--- TxtData()에서  CreateTexts() 호출시 keyCount가 44가 됩니다.
	그 다음에 Produce.cs의 Start()에서 UpdateTexts()호출하는데 이 때 keyCount가 0
	-> public static Dictionary<string, TextMeshProUGUI> textReferences = new Dictionary<string, TextMeshProUGUI>();
        으로 static으로 변경
	(다른 스크립트 produce.cs에서 SingletonManager.Instance.txtData.UpdateTexts(); 접근하려면 static 필요)
5.21
	ref SingletonManager.Instance.data.currentReceivable); currentReceivable이 get을 이용한 property로 바뀌었으면 ref 쓸 수 없음
	    public float currentReceivable
   	 {        get { return Receivable; }
        set { Receivable = value; }    }
	이 경우 그냥 currentReceivable 사용
	totalFlow  = FinFlowSummary(finFlowDirectTxt, finFlowImage) // 이걸 실행하네
	FinFlowSummary()가 float 메서드로 return CFF;를 반환하는데 이 메서드를 실행하고 값을 반환하고 있음. 
	void로 바꾸고  CFF를 전역변수로  CFF = cap.cashFromCapital + liq.cashFromLiquidDebt + illiq.cashFromIlliquidDebt; 사용
5.30
	시작시 illiquidGameObject와  LiquidGameObject가 파괴됨. DebtImageController 의 싱글톤문구 else(Destroy)에 의함
	> Inspector 에 스크립트 할당을  illiquidGameObject에만 하고, LiquidGameObject에[서는 삭제(uncheck 불충분)
        > UIObjectManager.Instance.illiquidDebtGameObject. 사용
	시작시 receivableGameObject 가 파괴. capitalImg에 붙어 있는 capitalMOve.cs가 여기에도 uncheck로 붙어 있음. 이거 삭제
	> 동일한 싱글톤 스크립트가 두군데 붙어있으면 안됨(	LiquidGameObject, illiquidGameObject <- DebtImageController)
6.03
	버튼, TMP_InputField ->홧살표키로 버튼 이동, 스페이스키로 실행(submit) -> 이건 기본 기능
	-> eDITOR 폴더에 SetNavigationNone 스크립트 적용하여 해결. 버튼의 Navigation 옵션 None으로 설정
6.04
	SingletonCanvas -> IlliquidDebt -> SingletonCanvas로 부모를 바꿀 때 부모설정을 먼저 하고 orogonalPosition 적용
	 ; orogonalPosition을 먼저 적용할 경우 다른 부모 연계하여 위치가 설정되어 엉뚱한 위치가 됨
	같은 캔버스 SingletonCanvas 위에 있어야오브젝트가 보임. 다른 캔버스에 있으면 안 보인다.
6.05
	슬라이더의 색상 조정 : 슬라이더의 자식인 Background  색상 투명으로 조정
6.07
	CostNProfit 각 요소 결정메서드 정리 SetSecondParameter, ProcessInputData
  	손익계산서 과정 끝에서 자산과 부채자본 일치 <이자 계산시  Debt> Interest >Cash 순으로 계산
	<- 법인세계산시 Debt> Interest >EBT > Tax > && Interest 증가분 반영
6.09
	sales.CurrentSales에서 null reference error  발생
	    //public CostData costData; 이 부분 할당하지 않아서 에러 발생. 싱글톤일 경우 private로 하고 할당 안해도 됨.
        public float currentSales   
        { get => CostData.Instance.currentSales;
        set { CostData.Instance.currentSales = value; }   }
6.10
	json.NET 이용한 게임상태 저장/로딩
	CostData is missing the class attribute 'ExtensionOfNativeClass'!"  문제
	Library 폴더를 통째로 삭제해 봐도 안되었고, 유니티 재시작해도 안되고
 CostData 클래스를 통째로 삭제후 다시 만들어 봐도 안되었습니다. 
생각해 보니 CostData 클래스가 Monobeg\havior을 상속받는 클래스였을 때 오브젝트에 붙였었는데 순수 c#스크립트로 바꾸면서 그것을 그대로 두었었습니다. 순수 c#스크립트는 오브젝트에 붙일 필요가 없기 때문에 오브젝트에서 remove component 했더니 이제 에러가 나오지 않습니다. 
	Player가 마우스 클릭시 이동하지 않는 문제 발생. LayerMask를 everything으로 변경 설정하여 해결
	
6.12 SalesAnout에서  NullReferenceException 
	MatchingPositionAndSize(salesAmount); 살리고 sales.currentSales ->  CostData.Instance.currentSales로 변경
	Slider 와 canvas 할당해 주어야 회전 작동
6.21
	CreateTextElementsWithKeys와 UpdateTextValue 분리
	static으로 선언하여 전역에서 사용하기
	   public static string[] FinancialItems1 = { "Cash", "Receivable", "Inventory", "PPE", "Intangible", "Investment", "TotalAsset" };
            public static string[] FinancialItems2 = { "LiquidDebt", "IlliquidDebt", "Capital", "TotalCapital" };

6.23 Start()에서 Null 에러가 생기는 문제 Script 실행순서 조정 
	Unity 에디터 상단의 메뉴에서 Edit > Project Settings를 선택합니다.
	왼쪽 메뉴에서 Script Execution Order를 클릭합니다.
	"Script Execution Order" 패널에서 + 버튼을 클릭하여 새 실행 순서를 추가합니다. 	TxtData를 -100으로 설정(Default보다 빠르게)

7.04 GeValue의 data에서 null 에러가 생기는 문제
	TxtData에서 data가 txtData Update() 보다 빨리 초기화되도록 보장
	SingletonManager에 
    public event Action OnDataReady;  // 데이터 준비 완료 이벤트 선언
	    public void NotifyDataReady()
    {        OnDataReady?.Invoke();    }
	반영.
	TxtData에 
    void OnEnable()
    {        SingletonManager.Instance.OnDataReady += HandleDataReady;    }
    void HandleDataReady()
    {         UpdateTexts();    }

	 UpdateTexts(); 의 if (textReferences.ContainsKey(key)) 에 null error 발생
	CreateTextElementsWithKeys가 먼저 실행되어 textReferencesPanel1 이 먼저 초기화
    public void UpdateTexts()
    {
        if (textReferencesPanel1 == null || textReferencesPanel2 == null)
        {
            textReferencesPanel1 = CreateTextElementsWithKeys(parentPanel1, financialItems1, fixedWidth1, fixedHeight1);
            textReferencesPanel2 = CreateTextElementsWithKeys(parentPanel2, financialItems2, fixedWidth2, fixedHeight2);
        }
        UpdateTextValues(textReferencesPanel1, financialItems1);
        UpdateTextValues(textReferencesPanel2, financialItems2);
    }

7.07 
	1. CalculateMeanAndDifference 가 맞지 않은 문제 : lastData가 0으로 되어 있음
	   실행순서로 해결 SettingData Start()에서
	        SingletonManager.Instance.SetLastData();
        SingletonManager.Instance.SetRawData();
        SingletonManager.Instance.CalculateMeanAndDifference();

        SingletonManager.Instance.txtData.UpdateTexts();
	2. CalculateMeanAndDifference()에서는 이전 데이터 값 먼저 가져온 후 평균 계산
	실시간 계산 방법 : TxtData().UpdateTexts()에 반영
  	        if (sceneName == "NewScene") 
        { 
            SingletonManager.Instance.CalculateMeanAndDifference();
            //SingletonManager.Instance.SetRawData();//  PPE 감가상각 바뀌면 안됨
        }

7.08 CostNProfit의 example data 가 유지되지 않고 자동 계산되는 문제 
	UpdateCostValues)안에 자동 계산 로직 제거. Txt만 업데이트

7.15 TxtData 초기화
	NewScene의 AutoNaming오브젝트에 TxtData가 uncheck된 상태로 붙어있는데 여기에 
	parentPanel1, parentPanel2 이 인스펙터에서 할당이 되어 있었습니다. TxtData가 uncheck된 상태
	SaftyGame씬의 AutoNaming오브젝트에 TxtData가 uncheck된 상태에서  
	parentPanel1, parentPanel2 이 인스펙터에서 할당이 되어 있지 않은 차이가 있어 이것을 할당을 해보았더니 놀랍게도 작동이 됩니다.  
         Awake()에 
       if (parentPanel1 == null)
            {                parentPanel1 = GameObject.Find("ParentPanel1")?.transform; } 추가
	싱글톤 스크립트들을 인스펙터에서 할당하지 않고 FindObjectOfType 사용. 해당 스크립트 완전 제거
	1. ASingletonManager 오브젝트에서
  	SingletonManager, TxtData, GameCountManager 제거
	2. SingletonManager 스크립트에서
 	TxtData 참조 삭제
	3. NewScene > TxtData 초기화 

7.22 게임 데이터 변동
	UtilityTools에서 컨트롤 : ReduceDebtSize(), SetDebtImage, ReduceAssets()
 	gamespeed : 부채비율을 줄여나간다. (부채비율 400) gameSpeed 20이면 20회 필요

7.28 illiquidDebtGameObject reset시 위치 문제 : setParent 먼저 후 ResetToInitialState() 실행하니 해결
        UIObjectManager.Instance.liquidDebtGameObject.transform.SetParent(singletonObjectCanvasTransform);
        debtImageController.ResetToInitialState();

7.29   if (GameDataManager.Instance.data.currentLiquidDebt <= 0)
        {HandleGameOver(true);}
        private void HandleGameOver(bool gameResult) 적용

7.31 GameDataManager에 InitializeCountComponents() 제거하고 인스펙터에서 할당 방식 사용
          private void InitializeCountComponents()
    {        if (count == null)
        { count = gameObject.AddComponent<GameCountManager>(); }    } 아예 제거
8.09 BootStrap 무한반복 로그 발생. 
      Start에서 LoadStartScene > OnSceneSelected > SceneLoader1.Instance.LoadingScene(sceneName);
                  >         SceneManager.LoadScene(sceneName);  SceneManager.sceneLoaded += OnSceneLoaded;
                  > "StartScene"을 로드하니까 이게 Start를 다시 시작. 
           >         if (currentScene.name != StartSceneName) 추가

8.10 StartScene에서 MainScene 선택후 씬변경 버튼이 작동이 안됨  >  -= OnSceneLoaded; 제거
       public void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        AssignChangeSceneButton();
        //SceneManager.sceneLoaded -= OnSceneLoaded;
    }
  ㅇ ParentPanel1 찾기 및 초기화 :    Start()에서 하면 안되고 Awake에서 일찍 해야 함.   
          if (parentPanel1 == null)
        {
            GameObject canvas = GameObject.Find("UIFinTableCanvas");
            if (canvas != null)
            {
                parentPanel1 = canvas.transform.Find("ParentPanel1");}
      StartScene에서 데이터 디스플레이
                if (sceneName == "MainScene" || sceneName == "StartScene")  //  if (sceneName == "MainScene")
                {
                    data = SingletonManager.Instance.data;
                }
  ㅇ 게임씬 데이터가 0으로 디스플레이되는 문제
           try
        {  SingletonManager.Instance.data.SetCompanyData("example");
            sceneLoader1.CopyDataToGameData();} 가 제대로 복사 안됨
        Start()에서 싱글톤 반영하여        sceneLoader1 = SceneLoader1.Instance; 추가
  ㅇ UIObjectManager는 GameScene에서만 사용. 

8.17 GameData가 씬이 바뀔 때 디스플레이 안되는 문제 
      1> ParentPanel1에 LastPanel, CurrentPanel 등 자식들이 파괴된 문제. 
        bool isPanel2Empty = parentPanel2 == null || parentPanel2.childCount == 0;

        if (textReferencesPanel1 == null || textReferencesPanel2 == null || isPanel1Empty || isPanel2Empty)
        {
            UnityEngine.Debug.Log("EnsureUIComponentsCreated: Some panels are empty or uninitialized, recreating UI components.");

            // 필요한 패널이 비어 있거나 초기화되지 않았다면 다시 생성
            textReferencesPanel1 = CreateTextElementsWithKeys(parentPanel1, financialItems1, fixedWidth1, fixedHeight1);
      2> ParentPanel1 할당
	    public void TryFindPanels()
    {  // Retrieve the panels from the TxtData instance
        Transform parentPanel1 = TxtData.Instance.parentPanel1;
        parentPanel1 = GameObject.Find("ParentPanel1")?.transform; }

8.22 SceneLoader1이 SettingData보다 먼저 실행되지 못하고 ChangeScene버튼, StartScene으로전환버튼이 작동이 안되는 문제	
 	각 씬에 오브젝트를 만들어 CallOrder.cs를 붙임(Instance는 Execution Order가 작동 안함)
public class InstanceCallorder : MonoBehaviour
{
    void Awake()
    {        if (SceneLoader1.Instance == null)
        {            var _ =  SceneLoader1.Instance;        }    }
}

8.27 CostNProfit.Instance는 생성되지만 currentSales 는 null이 나오는 문제 :
	CostNProfit이 CostData에  값을 복사하기 위해 CostData에 접근할 때 CostData가 초기화되어 있어야 한다.
        CostData 초기화를 먼저 하고 그 다음에 CostNProfit을 초기화. 
8.28 menu_up에 재무/투자/영업으로 관리 
9.04   SettingData 클래스의 bool isSet에 대한 접근 .. SettingData가 
        싱글톤일 경우 : SettingData,Instance.isSet 로 접근
	static Class일 경우 : SettingData,isSet로 접근
        일반 클래스일 경우 :  settingData,isSet로 접근 (public SettingData settingData; 인스펙터에서 할당)

	프로젝트가 실행되자마자 스크립트가 uncheck되는 문제 : Null error가 발생하는 경우 스크립트가 uncheck되어 또 다른 문제를 발생시킴
	  CostNProfit  Instance.currentSalesTxt = GameObject.Find("currentSalesText").GetComponent<TextMeshProUGUI>();
에서
	 HierArchy 상의 이름 currentSalesTxt 가 currentSalesText 와 달라 Nul error 발생 > 해결한 후 실행하면 계속 체크되어 있음

9.06 StartScene에서 잘 디스플레이되던 MainScene 버튼을 클릭하여 씬이 전환되면 씬에서 사라지고 첨부1 인스펙터에서 보듯  
       CostTxtData들의 구성요소들이 Missing으로 됩니다. 
	1. CostTxtData 초기화
	2. if (Instance == null)일 때 TextMeshProUGUI 컴포넌트들을 초기화하는 문제 수정
	  if (Instance != null) 포함하여 항상 초기화하도록 수정. 씬이 바뀌면 새로운  씬의 오브젝트를 참조해야 하고 기존 참조는 연결해제됨(Null이어도 실행)

      
       ChangeScene() 내에서 AssignParentPanels()를 호출하면, 씬이 완전히 로드되기 전에 실행되어 참조가 유실될 위험이 있습니다.
따라서, SceneManager.sceneLoaded 이벤트를 활용하여 씬 전환 후 모든 것이 로드된 이후에 오브젝트 참조를 다시 설정하는 것이 가장 안전하고 권장되는 방법입니다. 이를 통해 씬 전환 시 발생하는 참조 유실 문제를 방지할 수 있습니다.

MainScene에서 GameScene로 전환될 때 데이터가 디스플레이되지 않는 문제 ::
         ChangeScene() 내에서 AssignParentPanels()를 호출하면, 씬이 완전히 로드되기 전에 실행되어 참조가 유실될 위험이 있습니다.
따라서, SceneManager.sceneLoaded 이벤트를 활용하여 씬 전환 후 모든 것이 로드된 이후에 오브젝트 참조를 다시 설정하는 것이 가장 안전하고 권장되는 방법입니다. 이를 통해 씬 전환 시 발생하는 참조 유실 문제를 방지할 수 있습니다.

	스크립트에서 아무리 바꿔도 안먹히고 인스펙터 값으로만 되는 경우 : 선언부가 아닌 sTart에서 설정
	  선언부에서     [SerializeField] private float activationDistance = 5f; 와 같이 하면 유니티를 종료했다 재 실행해도 Inspector의 값이 스크립트에서 설정된 값대로 안변하는데, 
	Start에서
    void Start()
    {
        activationDistance = 5.0f;
    }
	와 같이 하면 실행할 때 5.0f로 초기화 됨.
9.08 TurnOver 회전율게임에서 자기자본, 재고자산이 사라지는 문제 : Starting Point.x = infimity
	sales.currentSales 가 아직 설정되기 전이라서 0. costData.currentSales 사용하면 값이 40으로 나와 해결됨
	cost.costOfGoods = 0. 원인 체크.  cost.costOfGoods 가 아니라 costData.costOfGoods 사용해야 함.

9.13 패널안에 vertical layout으로 있는 구성요소가 안보이는 문제 : size 가 0,0,0 > 1, 1, 1로 Anchors (min, max) = (0, 1)
9.30 CostNProfit 버튼이  MainScene에서 제대로 작동하나 다른 씬에 갔다오면 참조가 깨지고 다시 돌아와도 회복되지 않음
       CostNProfit의 DontDestroyOnLoad(gameObject);를 제거하고, 다른 씬에서 CostNProfit 오브젝트를 제거하여 파괴되게 하고
     MainScene에 돌아왔을 때 다시 생성되게 함
10.1 줄바꿈에서 null error 발생
    162행의  null은  줄바꿈으로 연결되는 165행까지를 의미. 그렇면 165행의 -produce.cashFromProduce + sales.cashFromSales - cost.cashFromSGA 중에서 null이 나올 가능성

    메서드 안에서 값이 변경되는 경우 메서드 인자와 호출하는 곳에서 반드시 ref 사용
    ashFromSgaIntTax의 값을 ProcessTwoInputData에서 변경하고, 이 변경된 값을 호출한 곳에서도 반영되길 원한다면 ref를 사용하십시오.