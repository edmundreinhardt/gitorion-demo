**free
 ctl-opt AlwNull(*UsrCtl);

//****************************************************
// Native I/O files
//****************************************************
 dcl-f PRODUCTS DISK USROPN Rename(PRODUCTS :XPROD_t)  Keyed;
 dcl-f XPRODCAT DISK USROPN Rename(PRODUCTS :XPRODC_t) Keyed;

//****************************************************
// Global data
//****************************************************
 dcl-c ARRAYMAX      999;
 dcl-s FilesAreOpen  ind   inz(*OFF);
 dcl-ds prod_t qualified based(Template);
   prod  int(10);
   cat   int(10);
   title int(10);
   photo varchar(64);
   price packed(12:2);
 end-ds;

//****************************************************
// prototypes
//****************************************************
 dcl-pr open_files;

 dcl-pr product_all;
     Max                    Int(10: 0);
     Count                  Int(10: 0);
     Item                   likeds(prod_t) dim(ARRAYMAX);
 end-pr;

 dcl-pr product_search_cat;
     cat                    BinDec(9: 0);
     Max                    Int(10: 0);
     Count                  Int(10: 0);
     Item                   likeds(prod_t) dim(ARRAYMAX);
 end-pr;

 dcl-pr Main                ExtPgm('PRODUCT');
     myCat                  Int(10: 0);
     myMax                  Int(10: 0);
     myCount                Int(10: 0);
     findMe                 likeds(prod_t) dim(ARRAYMAX);
 end-pr;

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// main(): Control flow
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 dcl-pi Main;
     myCat                  Int(10: 0);
     myMax                  Int(10: 0);
     myCount                Int(10: 0);
     findMe                 likeds(prod_t) dim(ARRAYMAX);
 end-pi;

 // Mainline
        if myCat > 9;
          product_all(myMax:myCount:findMe);
        else;
          product_search_cat(myCat:myMax:myCount:findMe);
        endif;
        return; // *inlr = *on;


//****************************************************
// open_files(): Open files used by this srvpgm
//****************************************************
 dcl-proc open_files;
        if (FilesAreOpen);
           return;
        endif;

        open PRODUCTS;
        open XPRODCAT;

        FilesAreOpen=*ON;
        return;

        begsr *pssr;
           close *all;
           FilesAreOpen=*OFF;
        endsr;

 end-proc;


//****************************************************
//  product_all:
//    Routine to load the search items on disk.
//****************************************************
 dcl-proc product_all;
     dcl-pi product_all;
       Max                          Int(10: 0);
       Count                        Int(10: 0);
       Item                         likeds(prod_t) dim(ARRAYMAX);
     end-pi;
// vars
     dcl-s cat                      BinDec(9: 0) inz(0);
     dcl-ds PRODFILE1               likerec(XPRODC_t:*INPUT);

          open_files();
          Count = 0;
          setll cat XPRODCAT;
          read(n) XPRODCAT PRODFILE1;
          dow not %eof(XPRODCAT);
            if Count = Max;
              leave;
            endif;
            Count += 1;
            Item(Count).PROD     = PRODFILE1.PROD;
            Item(Count).CAT      = PRODFILE1.CAT;
            Item(Count).TITLE    = PRODFILE1.TITLE;
            Item(Count).PHOTO    = PRODFILE1.PHOTO;
            Item(Count).PRICE    = PRODFILE1.PRICE;
            read(n) XPRODCAT PRODFILE1;
          enddo;
 end-proc;

//****************************************************
//  product_search_cat:
//    Routine to load the search items on disk.
//****************************************************
 dcl-proc product_search_cat;
     dcl-pi product_search_cat;
       cat                          BinDec(9: 0);
       Max                          Int(10: 0);
       Count                        Int(10: 0);
       Item                         likeds(prod_t) dim(ARRAYMAX);
// vars
     dcl-ds PRODFILE1               likerec(XPRODC_t:*INPUT);

          open_files();
          Count = 0;
          setll cat XPRODCAT;
          reade(n) cat XPRODCAT PRODFILE1;
          dow not %eof(XPRODCAT);
            if Count = Max;
              leave;
            endif;
            Count += 1;
            Item(Count).PROD     = PRODFILE1.PROD;
            Item(Count).CAT      = PRODFILE1.CAT;
            Item(Count).TITLE    = PRODFILE1.TITLE;
            Item(Count).PHOTO    = PRODFILE1.PHOTO;
            Item(Count).PRICE    = PRODFILE1.PRICE;
            reade(n) cat XPRODCAT PRODFILE1;
          enddo;
 end-proc;
