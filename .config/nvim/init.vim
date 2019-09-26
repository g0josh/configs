
syntax on

call plug#begin('~/.config/nvim/plugged')
Plug 'davidhalter/jedi-vim'   " jedi for python
Plug 'ncm2/ncm2'              " awesome autocomplete plugin
Plug 'roxma/nvim-yarp'
Plug 'ncm2/ncm2-bufword'      " buffer keyword completion
Plug 'ncm2/ncm2-path'  
call plug#end()

" path to your python 
let g:python3_host_prog = '/usr/bin/python3'

" ncm2 settings
autocmd BufEnter * call ncm2#enable_for_buffer()
set completeopt=menuone,noselect,noinsert
" make it FAST
let ncm2#popup_delay = 5
let ncm2#complete_length = [[1,1]]
let g:ncm2#matcher = 'substrfuzzy'

" CTRL-C doesn't trigger the InsertLeave autocmd . map to <ESC> instead.
inoremap <c-c> <ESC>
set pumheight=5
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <silent> <expr> <CR> (pumvisible() && empty(v:completed_item)) ?  "\<c-y>\<cr>" : "\<CR>"
set shortmess+=c

"jedi options
let g:jedi#auto_initialization = 1
let g:jedi#completions_enabled = 0
let g:jedi#auto_vim_configuration = 0
let g:jedi#smart_auto_mappings = 0
let g:jedi#popup_on_dot = 1
let g:jedi#completions_command = ""
let g:jedi#show_call_signatures = "1"
let g:jedi#show_call_signatures_delay = 0
let g:jedi#use_tabs_not_buffers = 0
let g:jedi#show_call_signatures_modes = 'i'  " ni = also in normal mode
let g:jedi#enable_speed_debugging=1

" Remove all trailing whitespace by pressing C-S
nnoremap <C-S> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar><CR>
autocmd BufReadPost quickfix nnoremap <buffer> <CR> <CR>

set backspace=2
"set background=dark
hi Folded ctermbg=0
filetype plugin indent on
set encoding=utf-8
set number relativenumber
set cursorline
set t_Co=256
set clipboard+=unnamedplus
set ruler
set path+=**

set foldmethod=syntax

"Tabs and spacing
set autoindent
set cindent
set tabstop=4
set expandtab
set shiftwidth=4
set smarttab
nnoremap tn :tabnew<Space>
nnoremap <C-Tab> :tabn<CR>
nnoremap <C-S-Tab> :tabp<CR>
nnoremap tf :tabfirst<CR>
nnoremap tl :tablast<CR>

"Search
set hlsearch
set incsearch
set ignorecase
set smartcase
"set diffopt +=iwhite

