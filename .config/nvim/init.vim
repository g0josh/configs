
syntax on
"let mapleader = "\<Space>"

" pep8
au BufNewFile,BufRead *.py
    \set tabstop=4
    \set softtabstop=4
    \set shiftwidth=4
    \set textwidth=79
    \set expandtab
    \set autoindent
    \set fileformat=unix
    \set fdm=indent
au BufNewFile,BufRead *.json
    \set tabstop=4
    \set softtabstop=4
    \set shiftwidth=4
    \set textwidth=79
    \set expandtab
    \set autoindent
    \set fileformat=unix
    \set fdm=syntax

" Remove all trailing whitespace by pressing C-S
nnoremap <C-w> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar><CR>
autocmd BufReadPost quickfix nnoremap <buffer> <CR> <CR>

set backspace=2
hi Folded ctermbg=0
hi MatchParen ctermbg=1
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
set background=light
set cindent
set tabstop=4
set expandtab
set shiftwidth=4
set smarttab
noremap tn :tabnew<Space>
nnoremap <C-Tab> :tabn<CR>
nnoremap <C-S-Tab> :tabp<CR>
nnoremap tf :tabfirst<CR>
nnoremap tl :tablast<CR>
nnoremap <C-i> :set fdm=

"Search
set hlsearch
hi Search ctermbg=8
set incsearch
set ignorecase
set smartcase
"set diffopt +=iwhite

