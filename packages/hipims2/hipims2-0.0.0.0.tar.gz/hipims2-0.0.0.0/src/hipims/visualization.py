
def domain_show(self, title='Domain Map', show_split=False, **kwargs):
        """Show domain map of the object
        
        Args:
            title: string to set the figure titile, 'Domain Map' is the defualt
            show_split: logical, show split lines for multi-gpu division 
        
        Retrun:
            fig: figure handle
            ax: axis handle
        """
        obj_dem = copy.deepcopy(self.DEM)
        fig, ax = obj_dem.mapshow(title=title, cax_str='DEM(m)', **kwargs)
        cell_subs = self.Boundary.cell_subs
        legends = []
        if show_split:            
            if hasattr(self, 'Sections'):
                x_overlayed = []
                y_overlayed = []
                for obj_sub in self.Sections:
                    overlayed_subs = obj_sub.overlayed_cell_subs_global
                    rows = overlayed_subs[0]
                    cols = overlayed_subs[1]
                    X, Y = sub2map(rows, cols, self.DEM.header)
                    x_overlayed = np.append(x_overlayed, X)
                    y_overlayed = np.append(y_overlayed, Y)
                ax.plot(x_overlayed, y_overlayed, '.k')
                legends.append('Splitting cells')
            else:
                warnings.warn("show_split is only for multi-gpu model")
        num = 0
        for cell_sub in cell_subs:
            rows = cell_sub[0]
            cols = cell_sub[1]
            X, Y = sub2map(rows, cols, self.DEM.header)
            ax.plot(X, Y, '.')
            if num==0:
                legends.append('Outline cells')
            else:
                legends.append('Boundary '+str(num))
            num = num+1
        
        ax.legend(legends, edgecolor=None, facecolor=None, loc='best',
                  fontsize='x-small')
        return fig, ax
    
    def plot_rainfall_map(self, figname=None, method='sum', **kw):
        """plot rainfall map within model domain
        """
        fig, ax = self.Rainfall.plot_rainfall_map(method='sum', **kw)
        cell_subs = self._outline_cell_subs
        rows = cell_subs[0]
        cols = cell_subs[1]
        X, Y = sub2map(rows, cols, self.DEM.header)
        ax.plot(X, Y, '.k')
        return fig, ax 

    def plot_rainfall_curve(self, start_date=None, method='mean', **kw):
        """ Plot time series of average rainfall rate inside the model domain

        Args:
            start_date: a datetime object to give the initial datetime of rain
            method: 'mean'|'max','min','mean', method to calculate gridded
                rainfall over the model domain
        """
        fig, ax = self.Rainfall.plot_time_series(method, **kw)
        return fig, ax