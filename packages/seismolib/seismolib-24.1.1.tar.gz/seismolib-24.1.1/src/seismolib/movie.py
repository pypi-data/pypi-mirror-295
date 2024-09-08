def gif_movie(figs, dpi=720, crop='0.5c'): 
    
    """
    PyGMTのFigureオブジェクトのリストからGifアニメーションを作成する．Jupyter Notebook上で表示されるオブジェクトを返す．

    Parameters
    ----------
    figs : list of Figure
        PyGMTのFigureオブジェクトのリスト
    dpi : int, optional
        解像度 (default: 720)
    crop : str, optional
        余白のトリミング量 (default: '0.5c')

    Returns
    -------
    HTML : IPython.display.HTML
        Gifアニメーション
    """
    from IPython import display as dd
    import tempfile
    import base64
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, fig in enumerate(figs):
            figname = f'plot_{i:05d}.png'
            print(f'\rsaving figs ... ({(i+1)/len(figs)*100:5.1f}%)', end='')
            fig.savefig(os.path.join(tmpdir, figname), dpi=dpi, crop=crop)
        print(' Done.')
        
        cmd1 = f'ffmpeg -i {tmpdir}/plot_%5d.png '
        cmd2 = f' -vf "scale=800:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse" '
        cmd3 = f' {tmpdir}/out.gif > /dev/null 2>&1'
        print(f'making gif ... ', end='')
        os.system(cmd1 + cmd2 + cmd3)
        print(' Done.')
        
        with open(f'{tmpdir}/out.gif', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        
    return dd.HTML(f'<img src="data:image/gif;base64,{b64}" />')
    