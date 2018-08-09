%sample to run the function
%matlab -r "generate({'8','2','14'},{'X310_3123D78', 'X310_3124E4A','X310_3123D76','X310_3123D58'}, '1', 000e3, 100e3, 100e3, 5e3, 110e3, 25e3)"


% list of device names : X310_3123D7B, X310_3123D7D, X310_3123D7E, X310_3123D52, X310_3123D54, X310_3123D58, X310_3123D64, X310_3123D65, X310_3123D70, X310_3123D76, X310_3123D78,X310_3123D79, X310_3123D80, X310_3123D89, X310_3123EFE, X310_3124E4A
% list of distances : 2,8,14,20,26,32,38,44,50,56,62
% run : either 1/2
% filename: wifi_100_crane-gfi_1_dataset-122
%inputfiles = dir(fullfile('/home/shamnaz/Downloads/Darpa_rfml/wifi/', '**', '*.mat'));
%inputfiles2 = dir(fullfile('/home/shamnaz/Downloads/Darpa_rfml/oldwifi/5', '**', '*.mat'));
%inputfiles = [inputfiles1',inputfiles2']
train_begin = 000;
train_size = 4500;
test_begin = 4500;
test_size = 1000;
val_begin = 5500;
val_size = 300;
% train_begin = 000;
% train_size = 6500;
% test_begin = 6500;
% test_size = 2000;
% val_begin = 8500;
% val_size = 500;
parse(inputfiles,train_begin,train_size,test_begin,test_size,val_begin,val_size);
function parse(inputfiles,train_begin,train_size,test_begin,test_size,val_begin,val_size)

    for train_test=1:1:3 %(train 1 , test 2)
        if(train_test==1)
            M=train_begin;
            N=train_size;
        elseif(train_test==2)
            M=test_begin;
            N=test_size;
        elseif(train_test==3)
            M=val_begin;
            N=val_size;
        end
        tic
        L = N;
        w = 128;
        K=0;
        shft=1;
        kk=(L-w+1)*w;
        tmprxdispSym=zeros(N,1);
        rxdisplaySym=zeros(kk,1);
        MatrixData=zeros(kk*length(inputfiles),2);
    
    
        for dev=1:length(inputfiles)
            tmp(dev) = load(strcat(fullfile(inputfiles(dev).folder),'/',fullfile(inputfiles(dev).name)));
            complexinp = tmp(dev).complexSignal;
            complexData = complexinp';
            tmprxdispSym = complexData(M+1:M+N);
        %file{dev}= strcat('WiFi_air_',device_id{dev},'_', dist{distance}, 'ft_run', run);
        %x=load(file{dev}, 'wifi_rx_data');
        %tmprxdispSym=x.wifi_rx_data(M+1:M+N);
            saen1=[];
            parfor k1 = 1:shft:L-w+1
                datawin(k1,:) = k1:k1+w-1;
                saen1(k1,:) = tmprxdispSym(datawin(k1,:));
            end
            rxdisplaySym=reshape(saen1.', [], 1);
            MatrixData((dev-1)*kk+1:dev*kk,:)=[real(rxdisplaySym) imag(rxdisplaySym)];
        end
        
        toc
        if(train_test==1)
            savefile=strcat('IQ',num2str(length(inputfiles)),'_', 'comb', 'ft_train_',num2str(N*length(inputfiles)),'K.mat');
        elseif(train_test==2)
            savefile=strcat('IQ',num2str(length(inputfiles)),'_', 'comb', 'ft_test_',num2str(N*length(inputfiles)),'K.mat');
        elseif(train_test==3)
            savefile=strcat('IQ',num2str(length(inputfiles)),'_', 'comb', 'ft_validation_',num2str(N*length(inputfiles)),'K.mat');
        end
	    
        save(savefile, 'MatrixData', '-v7.3' );
    end 
end
