             PGM        parm(&srcdir)
             dcl        &srcdir type(*char) len(100)
             dcl        &tgtlib type(*char) value('ORIONDEMO')
             dcl        &path type(*char) len(100)
             dcl        &pgm type(*char) value('getData')

/* Delete old objects */
             dltpgm     &tgtlib/&pgm
             monmsg     cpf0000

/* Create the  program */
             chgvar     &path (&srcdir *tcat '/' *tcat &pgm *tcat '.rpgle')
             crtbndrpg  srcstmf(&path) dbgview(*all)

             endpgm