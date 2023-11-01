import React from 'react';
import Fullpage,{ FullPageSections, FullpageSection, FullpageNavigation} from '@ap.cx/react-fullpage';

const FullPageScroll = () => {
    return(
        <Fullpage>
            <FullpageNavigation/>
            <FullPageSections>
                <FullpageSection style={{height: '100vh'}}>
                    <h1>Screan 1</h1>
                </FullpageSection>
                <FullpageSection style={{height: '100vh'}}>
                    <h1>Screan 2</h1>
                </FullpageSection>
                <FullpageSection style={{height: '100vh'}}>
                    <h1>Screan 3</h1>
                </FullpageSection>
                <FullpageSection style={{height: '100vh'}}>
                    <h1>Screan 4</h1>
                </FullpageSection>
            </FullPageSections>
        </Fullpage>
    );
};

export default FullPageScroll;