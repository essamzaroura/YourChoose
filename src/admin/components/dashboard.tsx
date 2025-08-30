import { Box, Button, Icon, Text, H2, H4, Link } from '@adminjs/design-system';
import React, { FC } from 'react';


const Dash: FC = () => {
  return (
      <Box flex flexDirection="column" alignItems="center" justifyContent="center">
        <br />
        <br />
        <H2 fontWeight="bold">Welcome, Candidate!</H2>
        <H4 >Happy coding and good luck, may the Force be with you!</H4>

        
      </Box>
  );
};

export { Dash };
export default Dash;
