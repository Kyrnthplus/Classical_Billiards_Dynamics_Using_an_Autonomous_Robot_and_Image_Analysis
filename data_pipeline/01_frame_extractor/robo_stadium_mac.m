% code updated on 23-Feb-2021
% this code analyzes the stadium video and
% obtains the arduino cart position
%
clear all;
close all;
tic;
VG=0; % View Graphics = 1 shows graphs, VG = 0 shows nothing

% cd('C:\Users\JOAO VICTOR\Videos\Area(4pi+1)\Circulo(r=0.9 a =0)\CirculoCurtos\CircAnti2dMap\Output1');
script_dir = fileparts(mfilename('fullpath'));
video_dir = fullfile(script_dir, '..', '..', 'data', 'raw', 'video', 'JPEG');
cd(video_dir);
% cd('/Users/antonio/Dropbox/projeto-carro/stadium/Stadium3/frames-gray');
fn=dir('*.jpg');
N=size(fn,1);
rx=NaN(1,N-1);
ry=NaN(1,N-1);

y0=545; % y-coordinate of the circle center
x0=754; % x-coordinate of the circle center
radius=465; % circle radius

% x0=94; % x-coordinate of the lower left corner
% y0=690; % y-coordinate of the lower left corner
% a=0*radius;%/2;
% 
% h=2*a;
% w=2*radius;%rectangle width
% 
% ht=2.0*radius;% rectangle height
% xrec=[x0 x0+w x0+w x0];
% yrec=[y0 y0 y0+ht y0+ht];

xm=751; %cond1
ym=764; %cond1

%xm=369; %cond2
%ym=1153; %cond2

%xm=301; %cond3
%ym=1182; %cond3

%xm=371; %cond4
%ym=1013; %cond4

%xm=336; %cond5
%ym=845; %cond5

%xm=839; %cond6
%ym=954; %cond6

sb=20; % sensitivity

xpos=NaN(1,N);
ypos=NaN(1,N);
xerro=NaN(1,N);
yerro=NaN(1,N);

filen = imread(fn(1).name);
if size(filen, 3) == 3
    PB = rgb2gray(filen);
else
    PB = filen;
end

% [lx,ly]=size(PB(:,:,1));
% 
% iimax=max(yrec);
% iimin=min(yrec);
% jjmax=max(xrec);
% jjmin=min(xrec);
% 
% R0=uint8(zeros(lx,ly));
% for ii=1:lx
%     for jj=1:ly
%         if ii>iimin && ii<iimax && jj>jjmin && jj<jjmax
%             R0(ii,jj)=1;
%         end
%         
%     end
% end
yv=1:size(PB,1);
xv=1:size(PB,2);
[X,Y]=meshgrid(xv,yv);
R=sqrt((X-x0).^2+(Y-y0).^2);
R0=uint8(R<radius);

if VG==1
    figure(1)
    
    subplot(1,4,1)
    pcolor(PB);
    shading flat;
    axis equal tight;
    axis off;
    title('PB pcolor');
    
    subplot(1,4,2)
    pcolor(R0);
    shading flat;
    axis equal tight;
    axis off;
    title('Stadium');
    
    subplot(1,4,3)
    
    pcolor(R0.*PB);
    shading flat;
    axis equal tight;
    axis off;
    title('Zona alvo');
    
    subplot(1,4,4)
    imshow(PB);
    set(gca,'YDir','normal');
    set(gca,'XDir','normal');
    shading flat;
    axis equal tight;
    axis off;
    title('PB original');
    % lower left corner
    pos=[(x0) (y0) 2*radius (2*radius+2*a)];
    % (canto esquerdo inferior - x) (canto esquerdo inferior - y) largura
    % (largura)  (altura)
    
    hold on;
    rectangle('Position',pos,'Curvature',1,...
        'LineWidth',3,'EdgeColor',[1 0 0]);
    
    %     rectangle('Position',[x0 (y0+radius) w h],'EdgeColor',[1 1 0]); % central square
    %     rectangle('Position',[x0 (y0+radius) w w],'EdgeColor',[0 1 0],'Curvature',1); % upper circle
    %     rectangle('Position',[x0 (y0 ) w w],'EdgeColor',[0 0 1],'Curvature',1); % upper circle
    
    %     recpos=[x0 y0 w 3*radius];
    %     rectangle('Position',recpos,'EdgeColor','k'); % central square
    %
    axis equal
    
end
% NAO PRECISA SER DE 1 EM 1, ESTOU USANDO 10


for ii=1:1:N
    filen = imread(fn(ii).name);
    if size(filen, 3) == 3
        PB = rgb2gray(filen);
    else
        PB = filen;
    end
    
    disp(ii);
    
    PB=PB.*R0; % clears everything outside the stadium
    
    
    
    %     H(1) = figure; set(H,'visible','off'); %set(H,'color','none');
    % %     H.Position = [0 0 1920 1080];
    %     pcolor(R0.*PB);
    %     shading flat;
    %     axis equal tight;
    %     axis off;
    %     hold on;
    %     axis equal;
    %     saveas(H,['dig' num2str(ii) '.jpg']);
    %     close(H);
    
    xseek=(round(0.97*xm):round(1.03*xm));
    yseek=(round(0.97*ym):round(1.03*ym));
    
    PBaux=zeros(size(PB));
    PBaux(yseek,xseek)=PB(yseek,xseek);
    
    %maximum = max(PB(yseek,xseek));
    maximum=max(PBaux(:));
    [y,x]=find(PBaux>(maximum-sb));
    
    xm=mean(x);
    xstd=std(x);
    ym=mean(y);
    ystd=std(y);
    
    cond1=x>(xm-xstd);
    cond2=x<(xm+xstd);
    cond3=y>(ym-ystd);
    cond4=y<(ym+ystd);
    
    cond=cond1.*cond2.*cond3.*cond4;
    
    mx=cond.*x;
    my=cond.*y;
    
    mx=mx(mx~=0); % remove 0 elements, eles modificam as médias
    my=my(my~=0); % remove 0 elements
    
    xpos(ii)=mean(mx);
    ypos(ii)=mean(my);
    xerro(ii)=std(mx);
    yerro(ii)=std(my);
    
    %    CANNOT USE PLOT IN TERMINAL MODE
    
    if VG==1
        figure(2);
        pcolor(PBaux);
        shading flat;
        axis equal tight;
        axis off;
        title('Zona alvo');
%         imagesc(PB);
%         shading flat;
%         axis equal tight;
%         hold on;
%         %plot(mx,my,'.r');
%         plot(xpos(ii),ypos(ii),'.r');
        %     xlim([min(x)-100 max(x)+100]);
        %     ylim([min(y)-100 max(y)+100]);
%         pause(.5);
    end
    clear mx my;
    PBold=PB;
end
data=[xpos' ypos' xerro' yerro'];
% save robo.dat;
% save('robo.txt','data','-ascii');
% type robo.txt;


%cd('~/Dropbox/projeto-carro/stadium/matlab');


temp=clock;
hh=num2str(temp(4));
mm=num2str(temp(5));
ss=num2str(floor(temp(6)));
script_dir = fileparts(mfilename('fullpath'));
output_dir = fullfile(script_dir, '..', '..', 'data', 'raw');

temp1 = fullfile(output_dir, strcat('robo_stadium','-',date,'-',hh,'-',mm,'-',ss,'.txt'));
temp2 = fullfile(output_dir, strcat('robo_stadium','-',date,'-',hh,'-',mm,'-',ss,'.mat'));

save(temp1,'data','-ascii');
save(temp2,'data');


if VG==1
    figure(2)
    plot(xpos,ypos);
    axis equal;
end
toc;
