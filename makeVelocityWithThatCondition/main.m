%data = readtable("home/esl/kyuyong/erclAllInOne/data/date/01091158/categorizedData/01091158.xlsx");
voltage = table2array(data(:,"frontV")) + table2array(data(:,"backV")) + table2array(data(:,"trunkV"));
current = table2array(data(:,"frontC"));

power = voltage.*current;

motorVelocity = abs(table2array(data(:,"bMotorVelocity")));
minMotorOriginal = min(motorVelocity);
maxMotorOriginal = max(motorVelocity);
minNew = 0;
maxNew = 41;


% 각 행의 데이터를 독립적으로 스케일링
numRows = size(motorVelocity, 1);
velocity = zeros(numRows, 1);

for i = 1:numRows
    velocity(i) = (motorVelocity(i) - minMotorOriginal) / (maxMotorOriginal - minMotorOriginal) * (maxNew - minNew) + minNew;
end

clearvars minMotorOriginal maxMotorOriginal  numRows i motorVelocity

%% get power per velocity
temp = round(velocity);
set = [power, temp];
sorted = sortrows(set,2);
plot(sorted(:,1))

%%
mvdPower = movmean(power,500);
mvdSet = [mvdPower,temp];
mvdsorted = sortrows(mvdSet,2);
plot(mvdsorted(:,1))

% 그리드를 표시할 위치 설정
x_values = minNew:maxNew;

% 그래프 그리기
plot(sorted(:,1))
hold on
grid on % 그리드 표시

% x축 레이블 설정
xticks(x_values)

% 결과 출력