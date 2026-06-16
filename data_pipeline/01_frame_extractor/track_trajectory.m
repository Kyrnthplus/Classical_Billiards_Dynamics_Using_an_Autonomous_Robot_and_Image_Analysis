% code updated on 23-Feb-2021
% this code analyzes the stadium video and
% obtains the tracked object position by tracking the peak of luminosity
% step-by-step across the entire frame.
%
clear all;
close all;
tic;
VG=0; % View Graphics = 1 shows graphs, VG = 0 shows nothing

script_dir = fileparts(mfilename('fullpath'));
video_dir = fullfile(script_dir, '..', '..', 'data', 'raw', 'video', 'images');
cd(video_dir);

fn=dir('*.jpg');
N=size(fn,1);
rx=NaN(1,N-1);
ry=NaN(1,N-1);

filen = imread(fn(1).name);
if size(filen, 3) == 3
    PB = rgb2gray(filen);
else
    PB = filen;
end

try
    imshow(filen);
    title('Click on the robot''s LED/light to start tracking');
    [xm, ym] = ginput(1);
    close(gcf);
catch
    xm = 751;
    ym = 764;
    disp('Graphics not supported or ginput failed. Using default start coordinates.');
end

sb=20; % sensitivity

xpos=NaN(1,N);
ypos=NaN(1,N);
xerro=NaN(1,N);
yerro=NaN(1,N);

if VG==1
    figure(1)

    subplot(1,2,1)
    pcolor(PB);
    shading flat;
    axis equal tight;
    axis off;
    title('PB pcolor');

    subplot(1,2,2)
    imshow(PB);
    set(gca,'YDir','normal');
    set(gca,'XDir','normal');
    shading flat;
    axis equal tight;
    axis off;
    title('PB original');
    axis equal
end

for ii=1:1:N
    filen = imread(fn(ii).name);
    if size(filen, 3) == 3
        PB = rgb2gray(filen);
    else
        PB = filen;
    end

    disp(ii);

    % Define local search window around the previous position
    x_min = max(1, round(0.97*xm));
    x_max = min(size(PB, 2), round(1.03*xm));
    y_min = max(1, round(0.97*ym));
    y_max = min(size(PB, 1), round(1.03*ym));
    xseek = x_min:x_max;
    yseek = y_min:y_max;

    PBaux = zeros(size(PB));
    PBaux(yseek,xseek) = PB(yseek,xseek);

    % Find the maximum brightness in the local search window
    maximum = max(PBaux(:));
    [y,x] = find(PBaux > (maximum - sb));

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

    mx=mx(mx~=0); % remove 0 elements, as they modify the means
    my=my(my~=0); % remove 0 elements

    xpos(ii)=mean(mx);
    ypos(ii)=mean(my);
    xerro(ii)=std(mx);
    yerro(ii)=std(my);

    % Update tracking coordinates for the next step
    xm = xpos(ii);
    ym = ypos(ii);

    if VG==1
        figure(2);
        pcolor(PBaux);
        shading flat;
        axis equal tight;
        axis off;
        title('Tracked target area');
    end
    clear mx my;
    PBold=PB;
end

data=[xpos' ypos' xerro' yerro'];

temp=clock;
hh=num2str(temp(4));
mm=num2str(temp(5));
ss=num2str(floor(temp(6)));
script_dir = fileparts(mfilename('fullpath'));
output_dir = fullfile(script_dir, '..', '..', 'data', 'raw');

temp1 = fullfile(output_dir, strcat('trajectory','-',date,'-',hh,'-',mm,'-',ss,'.txt'));
temp2 = fullfile(output_dir, strcat('trajectory','-',date,'-',hh,'-',mm,'-',ss,'.mat'));

save(temp1,'data','-ascii');
save(temp2,'data');

if VG==1
    figure(2)
    plot(xpos,ypos);
    axis equal;
end
toc;
