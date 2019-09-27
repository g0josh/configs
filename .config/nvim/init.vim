
syntax on

call plug#begin('~/.local/share/nvim/plugged')
Plug 'ncm2/ncm2-jedi'       " jedi for python
Plug 'ncm2/ncm2'           " awesome autocomplete plugin
Plug 'roxma/nvim-yarp'
Plug 'ncm2/ncm2-bufword'   " buffer keyword completion
Plug 'ncm2/ncm2-path'      " path completion
Plug 'vim-syntastic/syntastic'
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
"inoremap <silent> <expr> <CR> (pumvisible() && empty(v:completed_item)) ?  "\<c-y>\<cr>" : "\<CR>"
set shortmess+=c

"jedi options
let g:jedi#auto_initialization = 1
let g:jedi#completions_enabled = 0
let g:jedi#auto_vim_configuration = 0
let g:jedi#smart_auto_mappings = 0
let g:jedi#popup_on_dot = 1
let g:jedi#completions_command = ""
let g:jedi#show_call_signatures = "2"
let g:jedi#show_call_signatures_delay = 0
let g:jedi#use_tabs_not_buffers = 1
let g:jedi#show_call_signatures_modes = 'i'  " ni = also in normal mode
let g:jedi#enable_speed_debugging=1
let g:jedi#popup_select_first = 1

let g:jedi#goto_command = "<leader>d"
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = ""
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>n"
let g:jedi#completions_command = "<C-Space>"
let g:jedi#rename_command = "<leader>r"

" syntastic
let g:syntastic_python_checkers = ['pylint']
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 1

" pep8
au BufNewFile,BufRead *.py
    \ set tabstop=4
    \ set softtabstop=4
    \ set shiftwidth=4
    \ set textwidth=79
    \ set expandtab
    \ set autoindent
    \ set fileformat=unix

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
set fileformat=unix

set foldmethod=indent

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

